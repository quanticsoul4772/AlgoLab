# Prompt Stitch — Site vitrine AlgoLab

## Contexte du projet

AlgoLab est un interpréteur de pseudocode pédagogique en français. Il permet à des étudiants débutants d'écrire et d'exécuter des algorithmes en pseudocode académique, avec des messages d'erreurs clairs et formateurs. Il se distribue sous forme de binaires standalone (Linux, Windows, macOS), de paquet Debian, et d'extension VS Code.

---

## Prompt Stitch

> Design a showcase website for **AlgoLab**, a French-language pedagogical pseudocode interpreter for beginners learning algorithms.
>
> **Target audience:** beginner students, teachers/trainers, and self-learners — no prior coding experience assumed.
>
> **Tone:** Clean, academic, reassuring. Approachable but professional. Not playful or gamified — think "serious educational tool" rather than "coding bootcamp game". Inspired by documentation sites like Astro, Lark, or Docusaurus, but warmer.
>
> **Color palette:**
> - Primary: deep navy blue (`#1B2A4A`) — trust, academia
> - Accent: vivid teal/cyan (`#00B4D8`) — highlight CTAs, inline code, interactive elements
> - Background: near-white (`#F8F9FA`) with light gray cards (`#EDF2F7`)
> - Code blocks: dark background (`#1E293B`) with syntax highlighting in cyan and amber
> - Text: dark charcoal (`#1A202C`), secondary gray (`#718096`)
>
> **Typography:**
> - Headlines: geometric sans-serif (e.g. Inter or DM Sans), bold, generous sizing
> - Body: readable sans-serif, 16–18px base
> - Code: monospace (e.g. JetBrains Mono or Fira Code), prominent in UI — code is a first-class citizen
>
> **Layout:** Single-page landing with clear section separations. Full-width hero, then alternating content sections. Max content width ~1100px, generous whitespace, mobile-responsive.
>
> ---
>
> **Page sections to design:**
>
> ### 1. Navigation bar
> Logo (left) — "AlgoLab" wordmark with a small terminal/lambda icon. Nav links: Télécharger, Documentation, Extension VS Code, GitHub. Sticky, minimal, clean.
>
> ### 2. Hero section (above the fold)
> - Large headline: **"Apprenez l'algorithmique avec un pseudo-code exécutable, simple et multi-plateforme."**
> - Subheadline: "AlgoLab transforme le pseudo-code en pratique concrète : vous écrivez, vous exécutez, vous comprenez vos erreurs."
> - Two CTAs side by side: primary button "Télécharger la dernière release" (teal fill) + secondary button "Démarrer en 5 minutes" (outline)
> - Below CTAs: small trust line — "Stable v1 · Binaire Linux / macOS / Windows · Extension VS Code incluse"
> - Right side of hero: a code editor mockup (dark card) showing a short `.algo` program with syntax highlighting:
>   ```
>   Variable x : Entier
>   Debut
>     x <- 5
>     Ecrire x
>   Fin
>   ```
>   Below the editor: a terminal output strip showing `> algolab test.algo` → `5`
>
> ### 3. "Pourquoi AlgoLab ?" — 3-column feature cards
> Three icon + title + description cards:
> - **Pédagogie avant tout** — Pseudo-code francophone, syntaxe lisible, progression idéale pour débutants.
> - **Feedback immédiat** — Exécution rapide et diagnostics explicites pour corriger les erreurs sans frustration.
> - **Multi-plateforme** — Un moteur unique, des releases prêtes à l'emploi sur Linux, macOS et Windows.
>
> ### 4. "Ce que vous obtenez" — Feature list with visual
> Left: bulleted feature list with checkmarks:
> - Moteur AlgoLab CLI
> - Exemples `.algo` prêts à tester
> - Extension VS Code : bouton Run, bouton Vérification, diagnostics dans le panneau Problems
>
> Right: VS Code window mockup showing the extension in action — `.algo` file open, underlined error in red, Problems panel visible at the bottom.
>
> ### 5. "Installation rapide" — OS tabs
> Three tabs: Linux · macOS · Windows (+ a fourth tab: Extension VS Code)
> Each tab shows a minimal step-by-step with copy-paste terminal commands in a dark code block. Clean tab UI, active tab in teal.
>
> ### 6. "Premier programme en 30 secondes" — Interactive demo feel
> Centered section, dark card, step-by-step:
> 1. Write the code (shown in editor block)
> 2. Run `algolab test.algo`
> 3. See output `5`
> Minimal animation feel — like a typed terminal demo.
>
> ### 7. "Pour qui ?" — 3 personas cards
> Three cards with avatar icon, role label, and short message:
> - **Étudiant** — "Tu installes, tu lances, tu comprends tes erreurs."
> - **Enseignant** — "Même moteur sur tous les postes + doc claire + extension VS Code."
> - **Auto-apprenant** — "Guide de démarrage + exemples + FAQ."
>
> ### 8. "Fiabilité et releases" — Trust section
> Centered: version badge, release frequency info, GitHub link. Two CTAs: "Voir les releases" + "Lire le changelog".
>
> ### 9. Footer CTA banner
> Dark navy background. Large centered headline: "Prêt à lancer votre premier programme ?"
> Two buttons: "Télécharger AlgoLab" (teal) + "Ouvrir la documentation" (outline white).
>
> ### 10. Footer
> Three columns: Links (Documentation, GitHub, Releases, FAQ) | Resources (Exemples, Extension VS Code, Guide d'utilisation) | About (description one-liner). Bottom bar: MIT license notice + "Fait pour l'enseignement."
>
> ---
>
> **Design constraints:**
> - Code blocks must look sharp and readable — this is a developer/education tool, code is always prominent
> - Use real pseudocode snippets from the project (not Lorem Ipsum)
> - Avoid heavy gradients or overly decorative elements — clarity over decoration
> - All French-language copy, no translation
> - Accessible contrast ratios (WCAG AA minimum)
> - Desktop + mobile breakpoints
