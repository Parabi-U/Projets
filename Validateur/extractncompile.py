import json
import sys
import os
import glob
import subprocess
import traceback
import shutil


def process_notebook(notebook_path, output_dir):
    """Extrait les cellules de code (sauf celles taguées 'test')
    et écrit un fichier .py dans `output_dir`. Retourne le chemin du .py.
    """
    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        code_cells = [
            cell.get("source", [])
            for cell in data.get("cells", [])
            if cell.get("cell_type") == "code"
            and "test" not in cell.get("metadata", {}).get("tags", [])
        ]

        base = os.path.splitext(os.path.basename(notebook_path))[0]
        output_py = os.path.join(output_dir, base + ".py")
        with open(output_py, "w", encoding="utf-8") as f:
            for src in code_cells:
                f.write("# --- Cellule ---\n")
                f.write("".join(src))
                f.write("\n\n")

        return output_py, None
    except Exception:
        return None, traceback.format_exc()


def run_script(py_path):
    """Exécute le fichier python et retourne (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            ["python3", py_path], capture_output=True, text=True
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def main():
    # dossier cible en argument ou le répertoire courant
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    if not os.path.isdir(target_dir):
        print(f"❌ Le chemin fourni n'est pas un dossier valide: {target_dir}")
        sys.exit(2)

    # dossier où placer les .py extraits
    python_extrait_dir = os.path.join(target_dir, "pythonExtrait")
    os.makedirs(python_extrait_dir, exist_ok=True)

    pattern = os.path.join(target_dir, "*.ipynb")
    notebooks = sorted(glob.glob(pattern))
    if not notebooks:
        print(f"Aucun fichier .ipynb trouvé dans {target_dir}.")
        return

    # 1) Extraction : écrire tous les .py dans python_extrait_dir
    generated = []
    summary = []
    for nb in notebooks:
        print(f"--- Extraction: {nb}")
        py_path, err = process_notebook(nb, python_extrait_dir)
        if err:
            print("❌ Erreur lors de l'extraction :")
            print(err)
            summary.append((nb, "extract_error"))
            continue

        print(f"✅ Généré : {py_path}")
        generated.append((nb, py_path))

    # 2) Copier les fichiers utilitaires dans python_extrait_dir
    support_files = [
        "utils/automateBase.py",
        "utils/myparser.py",
        "utils/sp.py",
        "utils/state.py",
        "utils/transition.py", 
    ]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\n--- Copie des fichiers utilitaires dans {python_extrait_dir} ---")
    for fname in support_files:
        src = os.path.join(script_dir, fname)
        dst = os.path.join(python_extrait_dir, fname.split("/")[1])
        if os.path.exists(src):
            try:
                shutil.copy2(src, dst)
                print(f"✅ {fname} copié.")
            except Exception as e:
                print(f"❌ Erreur copie {fname}: {e}")
        else:
            print(f"⚠️ Fichier manquant (non copié) : {src}")

    # 3) Exécution des scripts générés (dans python_extrait_dir)
    for nb, py_path in generated:
        print(f"--- Exécution: {py_path}")
        code, out, errout = run_script(py_path)
        if code == 0:
            print("✅ Exécution réussie :")
            print(out)
            summary.append((nb, "ok"))
        else:
            print("❌ Erreur pendant l'exécution :")
            print(errout)
            summary.append((nb, "runtime_error"))

    print("\n--- Récapitulatif ---")
    for nb, status in summary:
        print(f"{nb} -> {status}")


if __name__ == "__main__":
    main()
