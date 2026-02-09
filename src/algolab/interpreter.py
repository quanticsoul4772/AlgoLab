"""AST interpreter for AlgoLab."""

from __future__ import annotations

from ast import literal_eval
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Optional

from lark import Token, Tree

from .environment import Environment, TypeSpec
from .errors import AlgoLabError, RuntimeErrorAlgoLab, SemanticErrorAlgoLab
from .parser import parse_source


class Interpreter:
	"""Execute the Lark AST for AlgoLab."""

	def __init__(
		self,
		environment: Optional[Environment] = None,
		reader: Callable[[], str] = input,
		writer: Callable[[Any], None] = print,
	) -> None:
		self.environment = environment or Environment()
		self.reader = reader
		self.writer = writer
		self.functions: dict[str, FunctionDef] = {}

	def run(self, source: str) -> None:
		tree = parse_source(source)
		self.visit(tree)

	def visit(self, node: Tree) -> Any:
		method = getattr(self, f"visit_{node.data}", None)
		if method is None:
			raise RuntimeErrorAlgoLab(f"Noeud non supporte: {node.data}")
		try:
			return method(node)
		except AlgoLabError as exc:
			if exc.line is None:
				meta = getattr(node, "meta", None)
				if meta is not None and getattr(meta, "line", None) is not None:
					raise type(exc)(exc.raw_message, line=meta.line, column=meta.column) from exc
			raise

	def visit_programme(self, node: Tree) -> None:
		preamble = self._find_tree(node.children, "preamble")
		instructions = self._find_tree(node.children, "instructions")
		if preamble is not None:
			for child in preamble.children:
				if isinstance(child, Tree):
					self.visit(child)
		if instructions is not None:
			self.visit(instructions)

	def visit_fonction(self, node: Tree) -> None:
		name_token = self._find_token(node.children, "IDENTIFIER")
		if name_token is None:
			raise RuntimeErrorAlgoLab("Fonction invalide")
		params_node = self._find_tree(node.children, "params")
		return_type_node = self._find_tree(node.children, "type")
		body_node = self._find_tree(node.children, "instructions")
		return_expr = self._find_return_expr(node.children)
		if return_type_node is None or body_node is None or return_expr is None:
			raise RuntimeErrorAlgoLab("Fonction invalide")
		params = self._extract_params(params_node)
		return_type = self.visit(return_type_node)
		self.functions[name_token.value] = FunctionDef(
			name=name_token.value,
			params=params,
			return_type=return_type,
			body=body_node,
			return_expr=return_expr,
		)

	def visit_declarations(self, node: Tree) -> None:
		for child in node.children:
			if isinstance(child, Tree):
				self.visit(child)

	def visit_instructions(self, node: Tree) -> None:
		for child in node.children:
			if isinstance(child, Tree):
				self.visit(child)

	def visit_instruction(self, node: Tree) -> Any:
		for child in node.children:
			if isinstance(child, Tree):
				return self.visit(child)
		return None

	def visit_declaration(self, node: Tree) -> None:
		decl_list = self._find_tree(node.children, "decl_list")
		if decl_list is None:
			groups = [child for child in node.children if isinstance(child, Tree) and child.data == "decl_group"]
		else:
			groups = [child for child in decl_list.children if isinstance(child, Tree) and child.data == "decl_group"]
		if not groups:
			raise RuntimeErrorAlgoLab("Declaration invalide")
		for group in groups:
			self._declare_group(group)

	def visit_type(self, node: Tree) -> TypeSpec:
		token = self._first_token(node.children)
		if token is None:
			raise RuntimeErrorAlgoLab("Type invalide")
		type_name = token.value.upper()
		if type_name == "CHAINE":
			type_name = "CARACTERE"
		size_node = self._find_tree(node.children, "array_spec")
		size = None
		if size_node is not None:
			size_token = self._first_token(size_node.children)
			if size_token is None or size_token.type != "INT":
				raise RuntimeErrorAlgoLab("Taille de tableau invalide")
			size = int(size_token.value)
			if size <= 0:
				raise RuntimeErrorAlgoLab("Taille de tableau invalide")
		return TypeSpec(base=type_name, size=size)

	def _extract_params(self, node: Optional[Tree]) -> list[tuple[str, TypeSpec]]:
		if node is None:
			return []
		groups = [child for child in node.children if isinstance(child, Tree) and child.data == "param_group"]
		params: list[tuple[str, TypeSpec]] = []
		for group in groups:
			identifiers = self._find_tree(group.children, "identifiers")
			type_node = self._find_tree(group.children, "type")
			if identifiers is None or type_node is None:
				raise RuntimeErrorAlgoLab("Parametres invalides")
			type_spec = self.visit(type_node)
			for child in identifiers.children:
				if isinstance(child, Token) and child.type == "IDENTIFIER":
					params.append((child.value, type_spec))
		return params

	def _find_return_expr(self, children: Iterable[Any]) -> Optional[Tree]:
		seen_return = False
		for child in children:
			if isinstance(child, Token) and child.type == "RETOURNER":
				seen_return = True
				continue
			if seen_return and isinstance(child, Tree) and child.data == "expression":
				return child
		return None

	def _declare_group(self, node: Tree) -> None:
		identifiers = self._find_tree(node.children, "identifiers")
		type_node = self._find_tree(node.children, "type")
		if identifiers is None or type_node is None:
			raise RuntimeErrorAlgoLab("Declaration invalide")
		name_tokens = [
			child
			for child in identifiers.children
			if isinstance(child, Token) and child.type == "IDENTIFIER"
		]
		if not name_tokens:
			raise RuntimeErrorAlgoLab("Declaration invalide")
		type_spec = self.visit(type_node)
		for token in name_tokens:
			self.environment.declare(token.value, type_spec)

	def visit_affectation(self, node: Tree) -> None:
		assign_node = self._find_tree(node.children, "assignable")
		expr_node = self._find_tree(node.children, "expression")
		if assign_node is None or expr_node is None:
			raise RuntimeErrorAlgoLab("Affectation invalide")
		value = self._value(expr_node)
		name, index = self._resolve_assignable(assign_node)
		if index is None:
			self.environment.assign(name, value)
		else:
			self.environment.set_index(name, index, value)

	def visit_lire(self, node: Tree) -> None:
		args_node = self._find_tree(node.children, "lire_args")
		if args_node is None:
			raise RuntimeErrorAlgoLab("Instruction LIRE invalide")
		assign_node = self._find_tree(args_node.children, "assignable")
		if assign_node is None:
			raise RuntimeErrorAlgoLab("Instruction LIRE invalide")
		name, index = self._resolve_assignable(assign_node)
		type_name = self.environment.get_type(name)
		raw = self.reader().strip()
		value = self._parse_input(type_name, raw)
		if index is None:
			self.environment.assign(name, value)
		else:
			self.environment.set_index(name, index, value)

	def visit_ecrire(self, node: Tree) -> None:
		args_node = self._find_tree(node.children, "ecrire_args")
		if args_node is None:
			raise RuntimeErrorAlgoLab("Instruction ECRIRE invalide")
		values = self._value_children(args_node.children, skip_trees=set())
		if not values:
			raise RuntimeErrorAlgoLab("Instruction ECRIRE invalide")
		if len(values) == 1:
			self.writer(values[0])
			return
		text = " ".join(str(value) for value in values)
		self.writer(text)

	def visit_si(self, node: Tree) -> None:
		conditions: list[Any] = []
		blocks: list[Tree] = []
		else_block: Optional[Tree] = None
		pending_condition: Optional[Any] = None
		seen_sinon = False
		for child in node.children:
			if isinstance(child, Token) and child.type == "SINON":
				seen_sinon = True
				continue
			if isinstance(child, Tree) and child.data == "expression_booleenne":
				pending_condition = self._value(child)
				continue
			if isinstance(child, Tree) and child.data == "instructions":
				if pending_condition is not None:
					conditions.append(pending_condition)
					blocks.append(child)
					pending_condition = None
				elif seen_sinon:
					else_block = child
					seen_sinon = False

		if not blocks:
			raise RuntimeErrorAlgoLab("Instruction SI invalide")
		for condition, block in zip(conditions, blocks):
			if condition:
				self.visit(block)
				return
		if else_block is not None:
			self.visit(else_block)

	def visit_tant_que(self, node: Tree) -> None:
		children = node.children
		condition_node = self._find_tree(children, None)
		body = self._find_tree(children, "instructions")
		if condition_node is None or body is None:
			raise RuntimeErrorAlgoLab("Instruction TANT_QUE invalide")
		while self._value(condition_node):
			self.visit(body)

	def visit_pour(self, node: Tree) -> None:
		children = node.children
		name_token = self._find_token(children, "IDENTIFIER")
		body = self._find_tree(children, "instructions")
		if name_token is None or body is None:
			raise RuntimeErrorAlgoLab("Instruction POUR invalide")
		expr_nodes = [child for child in children if isinstance(child, Tree) and child.data not in {"instructions"}]
		if len(expr_nodes) < 2:
			raise RuntimeErrorAlgoLab("Instruction POUR invalide")
		start = self._value(expr_nodes[0])
		end = self._value(expr_nodes[1])
		step = self._value(expr_nodes[2]) if len(expr_nodes) > 2 else 1
		if step == 0:
			raise RuntimeErrorAlgoLab("Pas de boucle invalide: 0")
		current = start
		if step > 0:
			while current <= end:
				self.environment.assign(name_token.value, current)
				self.visit(body)
				current += step
		else:
			while current >= end:
				self.environment.assign(name_token.value, current)
				self.visit(body)
				current += step

	def visit_appel_fonction(self, node: Tree) -> Any:
		name_token = self._find_token(node.children, "IDENTIFIER")
		if name_token is None:
			raise RuntimeErrorAlgoLab("Appel de fonction invalide")
		function = self.functions.get(name_token.value)
		if function is None:
			raise RuntimeErrorAlgoLab(f"Fonction inconnue: {name_token.value}")
		args_node = self._find_tree(node.children, "arguments")
		arg_values = self._value_children(args_node.children, skip_trees=set()) if args_node else []
		if len(arg_values) != len(function.params):
			raise RuntimeErrorAlgoLab("Nombre d arguments invalide")

		previous_env = self.environment
		local_env = Environment(parent=previous_env)
		self.environment = local_env
		try:
			for (param_name, param_type), value in zip(function.params, arg_values):
				local_env.declare(param_name, param_type)
				local_env.assign(param_name, value)
			self.visit(function.body)
			result = self._value(function.return_expr)
			if function.return_type.is_array:
				raise RuntimeErrorAlgoLab("Retour de tableau non supporte")
			return local_env.coerce_value(function.return_type, result)
		finally:
			self.environment = previous_env

	def visit_expression(self, node: Tree) -> Any:
		return self._value(self._find_tree(node.children, None))

	def visit_expression_arithmetique(self, node: Tree) -> Any:
		return self._eval_infix(node.children, {"+": lambda a, b: a + b, "-": lambda a, b: a - b})

	def visit_terme(self, node: Tree) -> Any:
		return self._eval_infix(
			node.children,
			{
				"*": lambda a, b: a * b,
				"/": lambda a, b: a / b,
				"%": lambda a, b: a % b,
			},
		)

	def visit_facteur(self, node: Tree) -> Any:
		for child in node.children:
			if isinstance(child, Tree):
				return self._value(child)
			if isinstance(child, Token) and child.type in {"INT", "FLOAT", "IDENTIFIER", "STRING"}:
				return self._value(child)
		raise RuntimeErrorAlgoLab("Facteur invalide")

	def visit_array_access(self, node: Tree) -> Any:
		name_token = self._find_token(node.children, "IDENTIFIER")
		index_node = self._find_tree(node.children, "expression_arithmetique")
		if name_token is None or index_node is None:
			raise RuntimeErrorAlgoLab("Acces tableau invalide")
		index_value = self._value(index_node)
		return self.environment.get_index(name_token.value, index_value)

	def visit_expression_booleenne(self, node: Tree) -> Any:
		tokens = [child for child in node.children if isinstance(child, Token)]
		if tokens and tokens[0].value.upper() == "NON":
			operand = self._find_tree(node.children, None)
			if operand is None:
				raise RuntimeErrorAlgoLab("Expression booleenne invalide")
			return not bool(self._value(operand))
		comparateur = self._find_tree(node.children, "comparateur")
		logique = self._find_tree(node.children, "logique")
		if comparateur is not None:
			values = self._value_children(node.children, skip_trees={"comparateur"})
			if len(values) != 2:
				raise RuntimeErrorAlgoLab("Comparaison invalide")
			op = self.visit(comparateur)
			return self._apply_comparator(op, values[0], values[1])
		if logique is not None:
			values = self._value_children(node.children, skip_trees={"logique"})
			if len(values) != 2:
				raise RuntimeErrorAlgoLab("Expression logique invalide")
			op = self.visit(logique)
			if op == "ET":
				return bool(values[0]) and bool(values[1])
			return bool(values[0]) or bool(values[1])
		return self._value(self._find_tree(node.children, None))

	def visit_comparateur(self, node: Tree) -> str:
		token = self._first_token(node.children)
		if token is None:
			raise RuntimeErrorAlgoLab("Comparateur invalide")
		return token.value

	def visit_logique(self, node: Tree) -> str:
		token = self._first_token(node.children)
		if token is None:
			raise RuntimeErrorAlgoLab("Operateur logique invalide")
		return token.value.upper()

	def visit_nombre(self, node: Tree) -> Any:
		token = self._first_token(node.children)
		if token is None:
			raise RuntimeErrorAlgoLab("Nombre invalide")
		return self._value(token)

	def visit_booleen(self, node: Tree) -> bool:
		token = self._first_token(node.children)
		if token is None:
			raise RuntimeErrorAlgoLab("Booleen invalide")
		return token.value.upper() == "VRAI"

	def visit_chaine(self, node: Tree) -> str:
		token = self._first_token(node.children)
		if token is None:
			raise RuntimeErrorAlgoLab("Chaine invalide")
		return self._value(token)

	def _value(self, node: Any) -> Any:
		if isinstance(node, Tree):
			return self.visit(node)
		if isinstance(node, Token):
			if node.type == "IDENTIFIER":
				return self.environment.get(node.value)
			if node.type == "INT":
				return int(node.value)
			if node.type == "FLOAT":
				return float(node.value)
			if node.type == "STRING":
				return literal_eval(node.value)
			return node.value
		return node

	def _eval_infix(self, children: Iterable[Any], op_map: dict[str, Callable[[Any, Any], Any]]) -> Any:
		parts: list[Any] = []
		for child in children:
			if isinstance(child, Token) and child.value in op_map:
				parts.append(child.value)
			else:
				parts.append(self._value(child))
		if len(parts) == 1:
			return parts[0]
		if len(parts) % 2 == 0:
			raise RuntimeErrorAlgoLab("Expression invalide")
		result = parts[0]
		index = 1
		while index < len(parts):
			op = parts[index]
			right = parts[index + 1]
			if op in {"/", "%"} and right == 0:
				raise RuntimeErrorAlgoLab("Division par zero")
			if op == "+" and (isinstance(result, str) or isinstance(right, str)):
				result = f"{result}{right}"
			else:
				result = op_map[op](result, right)
			index += 2
		return result

	def _apply_comparator(self, op: str, left: Any, right: Any) -> bool:
		if op == "==":
			return left == right
		if op == "!=":
			return left != right
		if op == "<":
			return left < right
		if op == "<=":
			return left <= right
		if op == ">":
			return left > right
		if op == ">=":
			return left >= right
		raise RuntimeErrorAlgoLab(f"Comparateur inconnu: {op}")

	def _resolve_assignable(self, node: Tree) -> tuple[str, Optional[int]]:
		array_node = self._find_tree(node.children, "array_access")
		if array_node is not None:
			name_token = self._find_token(array_node.children, "IDENTIFIER")
			index_node = self._find_tree(array_node.children, "expression_arithmetique")
			if name_token is None or index_node is None:
				raise RuntimeErrorAlgoLab("Acces tableau invalide")
			index_value = self._value(index_node)
			return name_token.value, index_value
		name_token = self._find_token(node.children, "IDENTIFIER")
		if name_token is None:
			raise RuntimeErrorAlgoLab("Affectation invalide")
		return name_token.value, None

	def _find_token(self, children: Iterable[Any], token_type: str) -> Optional[Token]:
		for child in children:
			if isinstance(child, Token) and child.type == token_type:
				return child
		return None

	def _first_token(self, children: Iterable[Any]) -> Optional[Token]:
		for child in children:
			if isinstance(child, Token):
				return child
		return None

	def _find_tree(
		self,
		children: Iterable[Any],
		data: Optional[str],
		skip_names: Optional[set[str]] = None,
	) -> Optional[Tree]:
		for child in children:
			if isinstance(child, Tree):
				if skip_names and child.data in skip_names:
					continue
				if data is None or child.data == data:
					return child
		return None

	def _value_children(self, children: Iterable[Any], skip_trees: set[str]) -> list[Any]:
		values: list[Any] = []
		for child in children:
			if isinstance(child, Tree):
				if child.data in skip_trees:
					continue
				values.append(self._value(child))
			elif isinstance(child, Token):
				values.append(self._value(child))
		return values

	def _parse_input(self, type_name: str, raw: str) -> Any:
		if type_name == "ENTIER":
			try:
				return int(raw)
			except ValueError as exc:
				raise SemanticErrorAlgoLab("Entree invalide: entier attendu") from exc
		if type_name == "REEL":
			try:
				return float(raw)
			except ValueError as exc:
				raise SemanticErrorAlgoLab("Entree invalide: reel attendu") from exc
		if type_name == "CARACTERE":
			return raw
		if type_name == "BOOLEEN":
			raw_upper = raw.strip().upper()
			if raw_upper == "VRAI":
				return True
			if raw_upper == "FAUX":
				return False
			raise SemanticErrorAlgoLab("Valeur booleenne attendue (VRAI/FAUX)")
		raise SemanticErrorAlgoLab(f"Type inconnu: {type_name}")


@dataclass
class FunctionDef:
	name: str
	params: list[tuple[str, TypeSpec]]
	return_type: TypeSpec
	body: Tree
	return_expr: Tree
