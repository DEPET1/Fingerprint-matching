# Fingerprint-matching
Code for matching fingerprints based on minutiae points and similarity percentage.

# Porovnávání otisků prstů pomocí SIFT algoritmu

Tento projekt obsahuje kód pro porovnání otisků prstů pomocí SIFT (Scale-Invariant Feature Transform) algoritmu. SIFT detekuje klíčové body v obrázcích otisků prstů a porovnává je mezi sebou, aby určil podobnost mezi dvěma otisky. Tento kód lze použít pro různé účely, například pro identifikaci podezřelých na základě otisků prstů.

## Funkce

### `load_fingerprint(filename, base_dir='XXXXXX/database')`
Načte otisk prstu z databáze.

#### Parametry:
- `filename`: Název souboru s otiskem prstu (např. "Suspect1" nebo "Attacker1").
- `base_dir`: Cesta k adresáři, kde se nachází soubory s otisky.

#### Návratová hodnota:
Vrací obrázek otisku prstu, pokud je soubor nalezen, jinak `None`.

### `match_fingerprints(img1, img2, show_matches=False)`
Porovná dva otisky prstů pomocí SIFT algoritmu a vypočítá skóre podobnosti.

#### Parametry:
- `img1`: První otisk prstu.
- `img2`: Druhý otisk prstu.
- `show_matches`: Pokud je nastaveno na `True`, zobrazí se vizualizace shodných bodů.

#### Návratová hodnota:
Vrací skóre podobnosti (vyšší hodnota znamená větší podobnost).

### `compare_attacker_with_database(attacker_file="Attacker1.png", database_size=10, threshold=30, show_matches=False)`
Porovná otisk útočníka s databází otisků a vrátí seznam podezřelých, u kterých byla překročena hodnota podobnosti.

#### Parametry:
- `attacker_file`: Název souboru s otiskem útočníka.
- `database_size`: Počet otisků v databázi.
- `threshold`: Práh podobnosti pro pozitivní identifikaci.
- `show_matches`: Pokud je nastaveno na `True`, zobrazí se vizualizace shodných bodů.

#### Návratová hodnota:
Vrací seznam ID podezřelých a skóre podobnosti.

### `main()`
Příklad použití, který porovnává otisk útočníka s databází otisků.

## Instalace
1. Ujistěte se, že máte nainstalovaný Python 3.
2. Nainstalujte závislosti:
   ```bash
   pip install opencv-python numpy matplotlib
