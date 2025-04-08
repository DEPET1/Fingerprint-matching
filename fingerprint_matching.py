import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_fingerprint(filename, base_dir='XXXXXX/database'): # Nutno nahradit cestu k databázi otisků
    """
    Načte otisk prstu pro daný soubor s podporou různých formátů souborů.
    
    Args:
        filename: Název souboru nebo vzor (např. "Suspect1" nebo "Attacker1")
        base_dir: Základní adresář s otisky
    
    Returns:
        Načtený obrázek nebo None pokud soubor není nalezen
    """
    # Pokud filename obsahuje příponu, použijeme ho přímo
    if any(filename.endswith(ext) for ext in ['.png', '.bmp', '.jpg', '.jpeg']):
        full_path = os.path.join(base_dir, filename)
        if os.path.exists(full_path):
            img = cv2.imread(full_path)
            if img is not None:
                print(f"Úspěšně načten soubor: {full_path}")
                return img
        else:
            print(f"Soubor nenalezen: {full_path}")
            return None
    
    # Jinak zkusíme různé přípony
    extensions = ['.png', '.bmp', '.jpg', '.jpeg']
    for ext in extensions:
        full_path = os.path.join(base_dir, filename + ext)
        if os.path.exists(full_path):
            img = cv2.imread(full_path)
            if img is not None:
                print(f"Úspěšně načten soubor: {full_path}")
                return img
    
    print(f"Nelze najít nebo načíst otisk pro {filename}")
    return None

def match_fingerprints(img1, img2, show_matches=False):
    """
    Porovná dva otisky prstů pomocí SIFT algoritmu.
    
    Args:
        img1: První otisk prstu
        img2: Druhý otisk prstu
        show_matches: Zda zobrazit vizualizaci shodných bodů
    
    Returns:
        Skóre podobnosti (vyšší hodnota = větší podobnost)
    """
    # Inicializace SIFT detektoru
    sift = cv2.SIFT_create()
    
    # Detekce klíčových bodů a výpočet deskriptorů
    keypoints_1, descriptors_1 = sift.detectAndCompute(img1, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(img2, None)
    
    # Porovnání deskriptorů pomocí FLANN matcheru
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descriptors_1, descriptors_2, k=2)
    
    # Aplikace Lowe's ratio testu
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)
    
    # Zobrazení shod
    if show_matches and len(keypoints_1) > 0 and len(keypoints_2) > 0:
        img_matches = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        plt.figure(figsize=(12, 6))
        plt.imshow(img_matches)
        plt.title(f'Počet shod: {len(good_matches)}')
        plt.show()
    
    # Výpočet skóre podobnosti
    similarity_score = len(good_matches) / max(len(keypoints_1), len(keypoints_2), 1) * 100
    
    return similarity_score

def compare_attacker_with_database(attacker_file="Attacker1.png", database_size=10, threshold=30, show_matches=False):
    """
    Porovná otisk útočníka s databází otisků.
    
    Args:
        attacker_file: Název souboru s otiskem útočníka
        database_size: Počet otisků v databázi
        threshold: Práh podobnosti pro pozitivní identifikaci
        show_matches: Zda zobrazit vizualizaci shodných bodů
    
    Returns:
        Seznam ID podezřelých, které překročily práh podobnosti
    """
    # Načtení otisku útočníka
    attacker_dir = "XXXXXX/crime_scene"  # Předpokládáme, že Attacker1.png je přímo v XXXXXX
    attacker_image = load_fingerprint(attacker_file, attacker_dir)
    
    if attacker_image is None:
        print(f"Nelze načíst otisk útočníka: {attacker_file}")
        return []
    
    results = []
    
    # Porovnání se všemi otisky v databázi
    for i in range(1, database_size + 1):
        print(f"Porovnávám soubor {attacker_file} s Suspect{i}")
        
        # Příprava cesty k souboru s otiskem z databáze (zkusíme různé formáty)
        db_filename = f"Suspect{i}"
        db_image = load_fingerprint(db_filename)
        
        if db_image is not None:
            score = match_fingerprints(attacker_image, db_image, show_matches)
            print(f"Podobnost s Suspect{i}: {score:.2f}%")
            
            if score >= threshold:
                results.append((i, score))
    
    # Seřazení výsledků podle skóre
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def main():
    # Příklad použití - porovnání otisku útočníka s databází
    print("Porovnávání otisku útočníka s databází...")
    attacker_file = "Attacker1.png"
    database_size = 21     # Počet podezřelých v databázi
    threshold = 30         # Práh podobnosti (%)
    show_matches = True   # Nastavte na True pro zobrazení vizualizace shod
    
    matches = compare_attacker_with_database(attacker_file, database_size, threshold, show_matches)
    
    if matches:
        print("\nVýsledky porovnání:")
        for suspect_id, score in matches:
            print(f"Shoda s Suspect{suspect_id}: {score:.2f}%")
    else:
        print("\nŽádná shoda nenalezena nad prahem podobnosti.")

if __name__ == "__main__":
    main()