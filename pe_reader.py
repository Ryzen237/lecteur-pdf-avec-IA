#!/usr/bin/env python3
"""
Lecteur PE (Portable Executable) - Analyseur de fichiers exécutables Windows
Auteur: Assistant IA
Version: 1.0
"""

import struct
import sys
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import argparse

class PEReader:
    """Classe principale pour lire et analyser les fichiers PE"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = None
        self.dos_header = {}
        self.pe_header = {}
        self.optional_header = {}
        self.sections = []
        self.imports = []
        self.exports = []
        
    def load_file(self) -> bool:
        """Charge le fichier PE en mémoire"""
        try:
            with open(self.filepath, 'rb') as f:
                self.data = f.read()
            return True
        except Exception as e:
            print(f"Erreur lors du chargement du fichier: {e}")
            return False
    
    def parse_dos_header(self) -> bool:
        """Parse l'en-tête DOS"""
        if len(self.data) < 64:
            print("Fichier trop petit pour contenir un en-tête DOS")
            return False
        
        # Vérifier la signature DOS "MZ"
        dos_signature = struct.unpack('<H', self.data[0:2])[0]
        if dos_signature != 0x5A4D:  # "MZ"
            print("Signature DOS invalide")
            return False
        
        # Parser les champs importants de l'en-tête DOS
        self.dos_header = {
            'signature': dos_signature,
            'bytes_on_last_page': struct.unpack('<H', self.data[2:4])[0],
            'pages_in_file': struct.unpack('<H', self.data[4:6])[0],
            'relocations': struct.unpack('<H', self.data[6:8])[0],
            'size_of_header': struct.unpack('<H', self.data[8:10])[0],
            'min_extra_paragraphs': struct.unpack('<H', self.data[10:12])[0],
            'max_extra_paragraphs': struct.unpack('<H', self.data[12:14])[0],
            'initial_ss': struct.unpack('<H', self.data[14:16])[0],
            'initial_sp': struct.unpack('<H', self.data[16:18])[0],
            'checksum': struct.unpack('<H', self.data[18:20])[0],
            'initial_ip': struct.unpack('<H', self.data[20:22])[0],
            'initial_cs': struct.unpack('<H', self.data[22:24])[0],
            'relocation_table_offset': struct.unpack('<H', self.data[24:26])[0],
            'overlay_number': struct.unpack('<H', self.data[26:28])[0],
            'pe_header_offset': struct.unpack('<I', self.data[60:64])[0]
        }
        
        return True
    
    def parse_pe_header(self) -> bool:
        """Parse l'en-tête PE"""
        pe_offset = self.dos_header['pe_header_offset']
        
        if pe_offset + 24 > len(self.data):
            print("Offset PE invalide")
            return False
        
        # Vérifier la signature PE "PE\0\0"
        pe_signature = struct.unpack('<I', self.data[pe_offset:pe_offset+4])[0]
        if pe_signature != 0x00004550:  # "PE\0\0"
            print("Signature PE invalide")
            return False
        
        # Parser l'en-tête COFF
        coff_offset = pe_offset + 4
        self.pe_header = {
            'signature': pe_signature,
            'machine': struct.unpack('<H', self.data[coff_offset:coff_offset+2])[0],
            'number_of_sections': struct.unpack('<H', self.data[coff_offset+2:coff_offset+4])[0],
            'time_date_stamp': struct.unpack('<I', self.data[coff_offset+4:coff_offset+8])[0],
            'pointer_to_symbol_table': struct.unpack('<I', self.data[coff_offset+8:coff_offset+12])[0],
            'number_of_symbols': struct.unpack('<I', self.data[coff_offset+12:coff_offset+16])[0],
            'size_of_optional_header': struct.unpack('<H', self.data[coff_offset+16:coff_offset+18])[0],
            'characteristics': struct.unpack('<H', self.data[coff_offset+18:coff_offset+20])[0]
        }
        
        return True
    
    def parse_optional_header(self) -> bool:
        """Parse l'en-tête optionnel"""
        pe_offset = self.dos_header['pe_header_offset']
        optional_offset = pe_offset + 24  # 4 (signature) + 20 (COFF header)
        
        if self.pe_header['size_of_optional_header'] == 0:
            return True
        
        if optional_offset + self.pe_header['size_of_optional_header'] > len(self.data):
            print("En-tête optionnel tronqué")
            return False
        
        # Magic number pour déterminer PE32 ou PE32+
        magic = struct.unpack('<H', self.data[optional_offset:optional_offset+2])[0]
        is_pe32_plus = magic == 0x20b
        
        self.optional_header = {
            'magic': magic,
            'major_linker_version': struct.unpack('<B', self.data[optional_offset+2:optional_offset+3])[0],
            'minor_linker_version': struct.unpack('<B', self.data[optional_offset+3:optional_offset+4])[0],
            'size_of_code': struct.unpack('<I', self.data[optional_offset+4:optional_offset+8])[0],
            'size_of_initialized_data': struct.unpack('<I', self.data[optional_offset+8:optional_offset+12])[0],
            'size_of_uninitialized_data': struct.unpack('<I', self.data[optional_offset+12:optional_offset+16])[0],
            'address_of_entry_point': struct.unpack('<I', self.data[optional_offset+16:optional_offset+20])[0],
            'base_of_code': struct.unpack('<I', self.data[optional_offset+20:optional_offset+24])[0],
        }
        
        if not is_pe32_plus:
            # PE32
            self.optional_header['base_of_data'] = struct.unpack('<I', self.data[optional_offset+24:optional_offset+28])[0]
            self.optional_header['image_base'] = struct.unpack('<I', self.data[optional_offset+28:optional_offset+32])[0]
            data_dirs_offset = optional_offset + 96
        else:
            # PE32+
            self.optional_header['image_base'] = struct.unpack('<Q', self.data[optional_offset+24:optional_offset+32])[0]
            data_dirs_offset = optional_offset + 112
        
        # Répertoires de données
        self.optional_header['section_alignment'] = struct.unpack('<I', self.data[optional_offset+32:optional_offset+36])[0]
        self.optional_header['file_alignment'] = struct.unpack('<I', self.data[optional_offset+36:optional_offset+40])[0]
        
        return True
    
    def parse_sections(self) -> bool:
        """Parse les sections"""
        pe_offset = self.dos_header['pe_header_offset']
        sections_offset = pe_offset + 24 + self.pe_header['size_of_optional_header']
        
        self.sections = []
        for i in range(self.pe_header['number_of_sections']):
            section_offset = sections_offset + (i * 40)
            
            if section_offset + 40 > len(self.data):
                break
            
            name = self.data[section_offset:section_offset+8].rstrip(b'\x00').decode('ascii', errors='ignore')
            
            section = {
                'name': name,
                'virtual_size': struct.unpack('<I', self.data[section_offset+8:section_offset+12])[0],
                'virtual_address': struct.unpack('<I', self.data[section_offset+12:section_offset+16])[0],
                'size_of_raw_data': struct.unpack('<I', self.data[section_offset+16:section_offset+20])[0],
                'pointer_to_raw_data': struct.unpack('<I', self.data[section_offset+20:section_offset+24])[0],
                'pointer_to_relocations': struct.unpack('<I', self.data[section_offset+24:section_offset+28])[0],
                'pointer_to_line_numbers': struct.unpack('<I', self.data[section_offset+28:section_offset+32])[0],
                'number_of_relocations': struct.unpack('<H', self.data[section_offset+32:section_offset+34])[0],
                'number_of_line_numbers': struct.unpack('<H', self.data[section_offset+34:section_offset+36])[0],
                'characteristics': struct.unpack('<I', self.data[section_offset+36:section_offset+40])[0]
            }
            
            self.sections.append(section)
        
        return True
    
    def get_machine_type(self) -> str:
        """Retourne le type de machine"""
        machine_types = {
            0x0: "Unknown",
            0x14c: "Intel 386",
            0x14d: "Intel 486",
            0x14e: "Intel Pentium",
            0x160: "MIPS R3000",
            0x162: "MIPS R3000 (little endian)",
            0x166: "MIPS R4000 (little endian)",
            0x168: "MIPS R10000 (little endian)",
            0x169: "MIPS WCE v2 (little endian)",
            0x184: "Alpha AXP",
            0x1a2: "Hitachi SH3",
            0x1a3: "Hitachi SH3 DSP",
            0x1a6: "Hitachi SH4",
            0x1a8: "Hitachi SH5",
            0x1c0: "ARM (little endian)",
            0x1c2: "ARM Thumb",
            0x1c4: "ARM Thumb-2 (little endian)",
            0x1d3: "Matsushita AM33",
            0x1f0: "PowerPC (little endian)",
            0x1f1: "PowerPC with floating point support",
            0x200: "Intel IA64",
            0x266: "MIPS16",
            0x284: "Alpha AXP 64-bit",
            0x366: "MIPS with FPU",
            0x466: "MIPS16 with FPU",
            0x8664: "AMD x64",
            0x9041: "Mitsubishi M32R (little endian)",
            0xaa64: "ARM64 (little endian)",
            0xc0ee: "clr pure MSIL"
        }
        return machine_types.get(self.pe_header['machine'], f"Unknown (0x{self.pe_header['machine']:x})")
    
    def get_characteristics(self) -> List[str]:
        """Retourne les caractéristiques du fichier"""
        characteristics = []
        flags = self.pe_header['characteristics']
        
        char_flags = {
            0x0001: "Relocation info stripped",
            0x0002: "Executable image",
            0x0004: "Line numbers stripped",
            0x0008: "Local symbols stripped",
            0x0010: "Aggressively trim working set",
            0x0020: "Large address aware",
            0x0080: "Little endian",
            0x0100: "32-bit machine",
            0x0200: "Debug info stripped",
            0x0400: "Removable run from swap",
            0x0800: "Net run from swap",
            0x1000: "System file",
            0x2000: "DLL",
            0x4000: "Uniprocessor only",
            0x8000: "Big endian"
        }
        
        for flag, desc in char_flags.items():
            if flags & flag:
                characteristics.append(desc)
        
        return characteristics
    
    def get_section_characteristics(self, characteristics: int) -> List[str]:
        """Retourne les caractéristiques d'une section"""
        section_chars = []
        
        char_flags = {
            0x00000020: "Contains code",
            0x00000040: "Contains initialized data",
            0x00000080: "Contains uninitialized data",
            0x02000000: "Contains comments",
            0x04000000: "Will not be cached",
            0x08000000: "Not pageable",
            0x10000000: "Shareable",
            0x20000000: "Executable",
            0x40000000: "Readable",
            0x80000000: "Writable"
        }
        
        for flag, desc in char_flags.items():
            if characteristics & flag:
                section_chars.append(desc)
        
        return section_chars
    
    def analyze(self) -> bool:
        """Analyse complète du fichier PE"""
        if not self.load_file():
            return False
        
        print(f"Analyse du fichier: {self.filepath}")
        print("=" * 50)
        
        if not self.parse_dos_header():
            return False
        
        if not self.parse_pe_header():
            return False
        
        if not self.parse_optional_header():
            return False
        
        if not self.parse_sections():
            return False
        
        return True
    
    def display_results(self):
        """Affiche les résultats de l'analyse"""
        print("\n🔍 EN-TÊTE DOS")
        print("-" * 30)
        print(f"Signature: {'MZ' if self.dos_header['signature'] == 0x5A4D else 'Invalide'}")
        print(f"Offset en-tête PE: 0x{self.dos_header['pe_header_offset']:08x}")
        
        print("\n🔍 EN-TÊTE PE")
        print("-" * 30)
        print(f"Signature: {'PE' if self.pe_header['signature'] == 0x00004550 else 'Invalide'}")
        print(f"Machine: {self.get_machine_type()}")
        print(f"Nombre de sections: {self.pe_header['number_of_sections']}")
        
        # Convertir timestamp
        timestamp = datetime.fromtimestamp(self.pe_header['time_date_stamp'])
        print(f"Date de compilation: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"Taille en-tête optionnel: {self.pe_header['size_of_optional_header']} bytes")
        
        print("\n📋 CARACTÉRISTIQUES")
        print("-" * 30)
        for char in self.get_characteristics():
            print(f"  • {char}")
        
        if self.optional_header:
            print("\n🔍 EN-TÊTE OPTIONNEL")
            print("-" * 30)
            print(f"Magic: 0x{self.optional_header['magic']:04x} ({'PE32+' if self.optional_header['magic'] == 0x20b else 'PE32'})")
            print(f"Version linker: {self.optional_header['major_linker_version']}.{self.optional_header['minor_linker_version']}")
            print(f"Taille du code: {self.optional_header['size_of_code']} bytes")
            print(f"Point d'entrée: 0x{self.optional_header['address_of_entry_point']:08x}")
            print(f"Base du code: 0x{self.optional_header['base_of_code']:08x}")
            print(f"Base de l'image: 0x{self.optional_header['image_base']:08x}")
        
        print("\n📂 SECTIONS")
        print("-" * 30)
        for i, section in enumerate(self.sections):
            print(f"\nSection {i+1}: {section['name']}")
            print(f"  Adresse virtuelle: 0x{section['virtual_address']:08x}")
            print(f"  Taille virtuelle: {section['virtual_size']} bytes")
            print(f"  Offset fichier: 0x{section['pointer_to_raw_data']:08x}")
            print(f"  Taille fichier: {section['size_of_raw_data']} bytes")
            
            chars = self.get_section_characteristics(section['characteristics'])
            if chars:
                print("  Caractéristiques:")
                for char in chars:
                    print(f"    • {char}")
        
        print(f"\n✅ Analyse terminée - {len(self.sections)} sections trouvées")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Lecteur PE - Analyseur de fichiers exécutables Windows")
    parser.add_argument("fichier", help="Chemin vers le fichier PE à analyser")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mode verbeux")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.fichier):
        print(f"Erreur: Le fichier '{args.fichier}' n'existe pas.")
        sys.exit(1)
    
    # Créer et utiliser le lecteur PE
    reader = PEReader(args.fichier)
    
    if reader.analyze():
        reader.display_results()
    else:
        print("Erreur lors de l'analyse du fichier PE")
        sys.exit(1)

if __name__ == "__main__":
    main()