import urllib.request
import urllib.error
import time
import sys
import os

URL = "https://cdn.luarmor.net/v4_init_marbeg.lua"
OUTPUT_FILE = "v4_init_marbeg.lua"
TIMEOUT = 10       # secondes
MAX_RETRIES = 3
RETRY_DELAY = 2    # secondes entre chaque tentative

HEADERS = {
    "User-Agent": "Roblox/WinInet",
    "Accept": "*/*",
}


def fetch(url: str, timeout: int = TIMEOUT) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        status = response.status
        content_type = response.headers.get("Content-Type", "inconnu")
        content = response.read().decode("utf-8")
        print(f"[OK] Status {status} | Content-Type: {content_type} | {len(content)} caractères")
        return content


def fetch_with_retry(url: str, max_retries: int = MAX_RETRIES) -> str | None:
    for attempt in range(1, max_retries + 1):
        try:
            print(f"[Tentative {attempt}/{max_retries}] Connexion à {url}...")
            return fetch(url)
        except urllib.error.HTTPError as e:
            print(f"[Erreur HTTP] {e.code}: {e.reason}")
            if e.code in (400, 401, 403, 404):
                print("[Abandon] Erreur non récupérable, pas de retry.")
                break
        except urllib.error.URLError as e:
            print(f"[Erreur réseau] {e.reason}")
        except TimeoutError:
            print("[Timeout] Le serveur n'a pas répondu à temps.")
        except UnicodeDecodeError:
            print("[Erreur] Impossible de décoder la réponse en UTF-8.")
            break

        if attempt < max_retries:
            print(f"[Attente] Nouvelle tentative dans {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)

    return None


def save(content: str, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[Sauvegardé] → {os.path.abspath(path)}")


def main() -> None:
    content = fetch_with_retry(URL)

    if content is None:
        print("[Échec] Impossible de récupérer le fichier.")
        sys.exit(1)

    # Affichage du contenu complet
    print("\n--- Contenu complet ---")
    print(content)
    print("---\n")

    # Sauvegarde optionnelle
    if "--save" in sys.argv or "-s" in sys.argv:
        save(content, OUTPUT_FILE)


if __name__ == "__main__":
    main()