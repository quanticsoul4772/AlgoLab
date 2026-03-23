const vscode = require('vscode');
const { spawnSync } = require('child_process');

function quoteArg(value) {
    if (process.platform === 'win32') {
        return `"${value.replace(/"/g, '\\"')}"`;
    }
    return `'${value.replace(/'/g, `'\\''`)}'`;
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    let disposable = vscode.commands.registerCommand('algolab.run', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage("Aucun fichier ouvert.");
            return;
        }

        const document = editor.document;
        if (document.languageId !== 'algolab') {
            vscode.window.showErrorMessage("Le fichier actif n'est pas un fichier AlgoLab (.algo).");
            return;
        }

        // Sauvegarder le fichier avant de lancer
        document.save().then(() => {
            const filePath = document.uri.fsPath;
            const executablePath = vscode.workspace
                .getConfiguration('algolab')
                .get('executablePath', 'algolab');

            const check = spawnSync(executablePath, ['--help']);
            if (check.error || check.status !== 0) {
                vscode.window.showErrorMessage(
                    "Impossible d'exécuter AlgoLab. Vérifiez `algolab.executablePath` et votre PATH."
                );
                return;
            }
            
            // Trouver ou créer un terminal
            let terminal = vscode.window.terminals.find(t => t.name === 'AlgoLab execution');
            if (!terminal) {
                terminal = vscode.window.createTerminal('AlgoLab execution');
            }
            
            terminal.show();
            // Lancer la commande algolab sur le fichier
            terminal.sendText(`${quoteArg(executablePath)} ${quoteArg(filePath)}`);
        });
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}
