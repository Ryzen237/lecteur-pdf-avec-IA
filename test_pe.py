#!/usr/bin/env python3
"""
Script de test pour le lecteur PE
Génère un fichier PE simple pour tester l'analyseur
"""

import os
import sys
from pe_reader import PEReader

def test_with_system_files():
    """Teste le lecteur PE avec des fichiers système disponibles"""
    print("🔍 Test du lecteur PE avec des fichiers système")
    print("=" * 50)
    
    # Fichiers système communs sur Linux qui pourraient contenir des PE
    test_paths = [
        "/usr/bin/python3",  # Binaire Linux (pas PE, mais pour tester la détection d'erreur)
        "/bin/ls",           # Binaire Linux (pas PE, mais pour tester la détection d'erreur)
    ]
    
    # Ajouter des chemins Windows si on est sur Windows/Wine
    if os.name == 'nt':
        test_paths.extend([
            "C:\\Windows\\System32\\notepad.exe",
            "C:\\Windows\\System32\\kernel32.dll",
            "C:\\Windows\\System32\\user32.dll"
        ])
    
    found_pe = False
    
    for filepath in test_paths:
        if os.path.exists(filepath):
            print(f"\n📁 Test avec: {filepath}")
            print("-" * 30)
            
            reader = PEReader(filepath)
            
            if reader.analyze():
                print("✅ Fichier PE valide détecté!")
                reader.display_results()
                found_pe = True
                break
            else:
                print("❌ Ce n'est pas un fichier PE valide (normal pour les binaires Linux)")
    
    if not found_pe:
        print("\n⚠️  Aucun fichier PE trouvé pour le test.")
        print("Pour tester avec de vrais fichiers PE:")
        print("1. Copiez un fichier .exe ou .dll Windows dans ce répertoire")
        print("2. Utilisez: python pe_reader.py <fichier.exe>")
        print("3. Ou lancez l'interface graphique: python pe_reader_gui.py")

def create_minimal_pe_demo():
    """Crée une démonstration avec des données PE simulées"""
    print("\n🔧 Démonstration de l'analyse des structures PE")
    print("=" * 50)
    
    # En-tête DOS minimal (structure)
    dos_header_info = {
        'signature': 0x5A4D,  # "MZ"
        'pe_header_offset': 0x80
    }
    
    # En-tête PE minimal (structure)
    pe_header_info = {
        'signature': 0x00004550,  # "PE\0\0"
        'machine': 0x14c,  # Intel 386
        'number_of_sections': 3,
        'time_date_stamp': 1640995200,  # 1 Jan 2022
        'characteristics': 0x102  # Executable + 32-bit
    }
    
    print("📋 Structure d'en-tête DOS:")
    print(f"  Signature: 0x{dos_header_info['signature']:04x} ({'MZ' if dos_header_info['signature'] == 0x5A4D else 'Invalid'})")
    print(f"  Offset PE: 0x{dos_header_info['pe_header_offset']:08x}")
    
    print("\n📋 Structure d'en-tête PE:")
    print(f"  Signature: 0x{pe_header_info['signature']:08x} ({'PE' if pe_header_info['signature'] == 0x00004550 else 'Invalid'})")
    
    # Types de machine
    machine_types = {
        0x14c: "Intel 386",
        0x8664: "AMD x64",
        0xaa64: "ARM64"
    }
    machine_name = machine_types.get(pe_header_info['machine'], f"Unknown (0x{pe_header_info['machine']:x})")
    print(f"  Machine: 0x{pe_header_info['machine']:04x} ({machine_name})")
    print(f"  Sections: {pe_header_info['number_of_sections']}")
    
    from datetime import datetime
    timestamp = datetime.fromtimestamp(pe_header_info['time_date_stamp'])
    print(f"  Compilé le: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Caractéristiques
    characteristics = pe_header_info['characteristics']
    print(f"  Caractéristiques: 0x{characteristics:04x}")
    
    char_flags = {
        0x0002: "Executable image",
        0x0100: "32-bit machine",
        0x2000: "DLL"
    }
    
    print("  Flags:")
    for flag, desc in char_flags.items():
        if characteristics & flag:
            print(f"    • {desc}")
    
    # Sections simulées
    sections = [
        {'name': '.text', 'size': 4096, 'characteristics': 0x60000020},  # Code
        {'name': '.data', 'size': 2048, 'characteristics': 0xC0000040},  # Data
        {'name': '.rsrc', 'size': 1024, 'characteristics': 0x40000040}   # Resources
    ]
    
    print(f"\n📂 Sections ({len(sections)}):")
    for i, section in enumerate(sections):
        print(f"\nSection {i+1}: {section['name']}")
        print(f"  Taille: {section['size']:,} bytes")
        print(f"  Caractéristiques: 0x{section['characteristics']:08x}")
        
        # Décoder les caractéristiques
        section_chars = []
        if section['characteristics'] & 0x20000000:
            section_chars.append("Executable")
        if section['characteristics'] & 0x40000000:
            section_chars.append("Readable")
        if section['characteristics'] & 0x80000000:
            section_chars.append("Writable")
        if section['characteristics'] & 0x00000020:
            section_chars.append("Contains code")
        if section['characteristics'] & 0x00000040:
            section_chars.append("Contains data")
        
        if section_chars:
            print("  Propriétés:")
            for char in section_chars:
                print(f"    • {char}")

def main():
    """Fonction principale de test"""
    print("🚀 LECTEUR PE - TESTS ET DÉMONSTRATIONS")
    print("=" * 60)
    
    # Test avec des fichiers système
    test_with_system_files()
    
    # Démonstration des structures
    create_minimal_pe_demo()
    
    print(f"\n{'=' * 60}")
    print("✅ Tests terminés!")
    print("\nPour utiliser le lecteur PE:")
    print("  • Ligne de commande: python pe_reader.py <fichier.exe>")
    print("  • Interface graphique: python pe_reader_gui.py")
    print("\nFormats supportés: .exe, .dll, .sys, .ocx et autres fichiers PE")

if __name__ == "__main__":
    main()