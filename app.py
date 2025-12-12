import sys
import os
import shutil
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QHBoxLayout, QMessageBox, QLabel, QMenuBar
from PyQt6.QtGui import QAction, QIcon, QPixmap, QActionGroup
from PyQt6.QtCore import Qt, QEvent, QSize

STYLE_SHEET = """
/* --- Global Styles --- */
QWidget {
    background-color: #FAFAFA; 
    color: #333333;            
    font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 14px;
}

/* --- Main Control Container --- */
#left_container {
    background-color: #FFFFFF;
    border-radius: 20px;
    border: 1px solid #E8E8E8; 
}

/* --- Input Field --- */
QLineEdit {
    background-color: #F7F8FA;
    border: 1px solid #E0E0E0;
    border-radius: 12px;
    padding: 10px 15px;
    color: #333;
    font-weight: 500;
}
QLineEdit:focus {
    border: 1px solid #5D9CEC;
    background-color: #FFFFFF;
}
QLineEdit:read-only {
    color: #666;
    background-color: #F0F2F5;
}

/* --- Primary Action Buttons --- */
#btn_sort, #btn_revert {
    background-color: #5D9CEC;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 14px;
}
#btn_sort:hover, #btn_revert:hover {
    background-color: #4A89DC;
}
#btn_sort:pressed, #btn_revert:pressed {
    background-color: #3A79CB;
    padding-top: 11px;
    padding-bottom: 9px;
}

/* --- Secondary Buttons --- */
#btn_open, #btn_lang {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 12px;
    color: #555;
}
#btn_open:hover, #btn_lang:hover {
    background-color: #F7F8FA; 
    border-color: #D0D0D0;
}
#btn_open:pressed, #btn_lang:pressed {
    background-color: #E0E0E0;
    border-color: #C0C0C0;
}

/* --- QMessageBox Styling --- */
QMessageBox {
    background-color: #FFFFFF;
}
QMessageBox QLabel {
    color: #333;
}

QMessageBox QPushButton {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 6px 15px;
    color: #555;
    font-weight: bold;
}
QMessageBox QPushButton:hover {
    background-color: #F7F8FA;
}
QMessageBox QPushButton:pressed {
    background-color: #E0E0E0;
}
"""

class FileSorter(QWidget):
    
    FILE_CATEGORIES = {
        "IMAGES": [
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".heic", 
            ".heif", ".ico", ".raw", ".psd", ".xcf", ".kra", ".ora", ".pdn", ".cpt", 
            ".psp", ".tga", ".dds", ".ppm", ".pgm", ".pbm", ".pnm", ".jp2", ".j2k", 
            ".jpf", ".jpx", ".jpm", ".mj2", ".iff", ".lbm",
            ".svg", ".svgz", ".ai", ".eps", ".cdr", ".wmf", ".emf", ".vsd", ".vsdx", 
            ".afd", ".design", ".sketch", ".fig",
            ".cr2", ".cr3", ".nef", ".nrw", ".arw", ".srf", ".sr2", ".orf", ".rw2", 
            ".raf", ".pef", ".srw", ".x3f", ".erf", ".mef", ".mos", ".dcs", ".dcr", 
            ".drf", ".k25", ".kdc", ".dng", ".3fr", ".ari", ".bay", ".cap", ".iiq", 
            ".eip", ".fff"
        ],
        "DOCUMENTS": [
            ".txt", ".md", ".markdown", ".rtf", ".tex", ".ltx", ".rst", ".adoc", 
            ".textile", ".nfo", ".log", ".err", ".sub", ".srt", ".vtt", ".ass", ".smi",
            ".doc", ".docx", ".docm", ".dot", ".dotx", ".dotm", ".odt", ".ott", ".fodt", 
            ".wps", ".wpd", ".pages", ".abw",
            ".xls", ".xlsx", ".xlsm", ".xlsb", ".xlt", ".xltx", ".xltm", ".ods", ".ots", 
            ".fods", ".csv", ".tsv", ".dif", ".numbers", ".slk", 
            ".ppt", ".pptx", ".pptm", ".pps", ".ppsx", ".ppsm", ".pot", ".potx", ".potm", 
            ".odp", ".otp", ".fodp", ".key", ".sxi",
            ".pdf", ".epub", ".mobi", ".azw", ".azw3", ".ibooks", ".djvu", ".cbr", 
            ".cbz", ".cb7", ".cbt", ".ind", ".indd", ".indt", ".idml", ".pmd", ".qxp", 
            ".pub", ".afpub"
        ],
        "AUDIO": [
            ".mp3", ".wav", ".flac", ".aac", ".ogg", ".oga", ".m4a", ".wma", ".aiff", 
            ".aif", ".aifc", ".alac", ".opus", ".ape", ".wv", ".mka", ".mpc", ".mp+", 
            ".mpp", ".tta", ".amr", ".awb", ".gsm", ".dct", ".dss", ".dvf", ".vox", 
            ".iklax", ".m4b", ".m4p", ".mmf", ".mpc", ".msv", ".nmf", ".nsf", ".ra", 
            ".rm", ".sln", ".w64",
            ".aup", ".aup3", ".logic", ".logicx", ".als", ".alp", ".cpr", ".npr", 
            ".flp", ".ptx", ".ptf", ".rpp", ".sesx", ".band"
        ],
        "VIDEO": [
            ".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm", ".m4v", ".3gp", 
            ".3g2", ".mpeg", ".mpg", ".mpe", ".mpv", ".m2v", ".m4v", ".svi", ".mxf", 
            ".roq", ".nsv", ".f4v", ".f4p", ".f4a", ".f4b", ".ogv", ".gifv", ".qt", 
            ".yuv", ".rm", ".rmvb", ".asf", ".amv", ".vob", ".mts", ".m2ts", ".ts",
            ".braw", ".r3d", ".ari", ".arx", ".cin", ".dpx", ".exr"
        ],
        "CODE": [
            ".html", ".htm", ".xhtml", ".css", ".scss", ".sass", ".less", ".js", ".jsx", 
            ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".wasm", ".php", ".asp", 
            ".aspx", ".jsp", ".cfm", ".cgi", ".pl", ".htaccess",
            ".py", ".pyw", ".pyc", ".pyd", ".java", ".class", ".jar", ".c", ".h", ".cpp", 
            ".hpp", ".cc", ".cxx", ".cs", ".csx", ".go", ".rb", ".rbw", ".rs", ".rlib", 
            ".swift", ".kt", ".kts", ".scala", ".groovy", ".lua", ".r", ".m", ".mm", 
            ".f", ".for", ".f90", ".f95", ".asm", ".s", ".v", ".sv", ".vhdl", ".nim", 
            ".ex", ".exs", ".erl", ".hrl", ".clj", ".cljs", ".hs", ".lhs", ".ml", ".mli", 
            ".fs", ".fsi", ".fsx", ".dart", ".pas", ".pp", ".d", ".julia", ".jl",
            ".json", ".json5", ".jsonc", ".xml", ".yaml", ".yml", ".toml", ".ini", 
            ".cfg", ".conf", ".properties", ".env", ".plist", ".config", ".reg", ".inf", 
            ".nix", ".dhall"
        ],
        "ARCHIVES": [
            ".zip", ".zipx", ".rar", ".7z", ".s7z", ".tar", ".gz", ".gzip", ".tgz", 
            ".bz2", ".bzip2", ".tbz2", ".xz", ".txz", ".lz", ".lzma", ".tlz", ".z", 
            ".taz", ".cpio", ".rpm", ".deb", ".ar", ".arj", ".cab", ".lzh", ".lha"
        ],
        "DISK_IMAGES": [
            ".iso", ".img", ".dmg", ".toast", ".vcd", ".cue", ".bin",
            ".vmdk", ".vdi", ".vhd", ".vhdx", ".hdd", ".qed", ".qcow", ".qcow2", ".ova", 
            ".ovf", ".vagrantfile", ".dockerfile"
        ],
        "EXECUTABLES": [
            ".exe", ".msi", ".com", ".scr", ".bat", ".cmd", ".vbs", ".vbe", ".jse", 
            ".wsf", ".wsh", ".ps1", ".ps1xml", ".ps2", ".ps2xml", ".psc1", ".psc2", 
            ".msc", ".sh", ".bash", ".zsh", ".fish", ".csh", ".ksh", ".awk", 
            ".sed", ".run", ".app", ".command", ".apk", ".aab", ".ipa", ".xap", 
            ".gadget", ".widget"
        ],
        "FONTS": [
            ".ttf", ".otf", ".woff", ".woff2", ".eot", ".pfb", ".pfm", ".afm", ".dfont", 
            ".ttc", ".fon", ".bmf"
        ],
        "3D_CAD": [
            ".obj", ".fbx", ".stl", ".dae", ".3ds", ".blend", ".max", ".ma", ".mb", 
            ".ply", ".gltf", ".glb", ".abc", ".usdz", ".usd", ".x3d", ".wrl", ".vrml", 
            ".lwo", ".lws", ".lxo", ".c4d", ".zpr", ".ztl", ".skp",
            ".dwg", ".dxf", ".dgn", ".step", ".stp", ".iges", ".igs", ".sat", ".sab", 
            ".brep", ".ipt", ".iam", ".catpart", ".catproduct", ".prt", ".asm", ".sldprt", 
            ".sldasm", ".fcstd", ".3dm", ".ifc"
        ],
        "DATABASE": [
            ".sql", ".db", ".sqlite", ".sqlite3", ".db3", ".s3db", ".mdf", ".ldf", 
            ".ndf", ".mdb", ".accdb", ".frm", ".ibd", ".myi", ".myd", ".dbf", ".nsf", 
            ".ntf", ".pdb", ".dmp", ".pgsql"
        ],
        "SCIENTIFIC": [
            ".dat", ".hdf", ".h4", ".hdf4", ".he2", ".h5", ".hdf5", ".he5", 
            ".nc", ".cdf", ".fits", ".sav", ".mat", ".rds", ".rdata", ".grib", ".grib2",
            ".shp", ".shx", ".kml", ".kmz", ".gpx", ".geojson", ".osm", ".asc", ".dem", 
            ".geotiff"
        ],
        "SYSTEM": [
            ".gpg", ".pgp", ".asc", ".enc", ".aes", ".axx", ".kdb", ".kdbx", ".vera", ".hc",
            ".bak", ".old", ".tmp", ".temp", ".swp", ".swo", ".ds_store", ".desktop", 
            ".lnk", ".pid", ".state", ".lock", ".sys", ".dll", ".so", ".o", ".a", ".dylib"
        ]
    }

    def __init__(self):
        super().__init__()
        
        self.translations = {
            'en': {
                'placeholder_text': "Choose a folder...",
                'sort_btn': "SORT",
                'revert_btn': "REVERT",
                'confirm_title': "Confirmation",
                'confirm_sort': "Are you sure you want to sort the files in this directory?",
                'confirm_revert': "Are you sure you want to revert folder changes in this directory?",
                'folder_names': {
                    "IMAGES": "Images",
                    "DOCUMENTS": "Documents",
                    "EXECUTABLES": "Executables",
                    "ARCHIVES": "Archives",
                    "VIDEO": "Video",
                    "AUDIO": "Audio",
                    "CODE": "Code",
                    "DISK_IMAGES": "Disk Images",
                    "FONTS": "Fonts",
                    "3D_CAD": "3D & CAD",
                    "DATABASE": "Database",
                    "SCIENTIFIC_GIS": "Scientific",
                    "SYSTEM": "System"
                }
            },
            'hu': {
                'placeholder_text': "Válassz egy mappát...",
                'sort_btn': "RENDEZÉS",
                'revert_btn': "VISSZAVONÁS",
                'confirm_title': "Megerősítés",
                'confirm_sort': "Biztosan rendezni szeretnéd a fájlokat ebben a mappában?",
                'confirm_revert': "Biztosan vissza szeretnéd vonni a mappaműveleteket?",
                'folder_names': {
                    "IMAGES": "Képek",
                    "DOCUMENTS": "Dokumentumok",
                    "EXECUTABLES": "Alkalmazások",
                    "ARCHIVES": "Tömörített",
                    "VIDEO": "Videók",
                    "AUDIO": "Hangfájlok",
                    "CODE": "Kódok",
                    "DISK_IMAGES": "Lemezképek",
                    "FONTS": "Betűtípusok",
                    "3D_CAD": "3D és CAD",
                    "DATABASE": "Adatbázisok",
                    "SCIENTIFIC_GIS": "Tudományos",
                    "SYSTEM": "Rendszerfájlok"
                }
            }
        }
        self.current_language = 'hu'

        self.setWindowTitle("FileOrganizer")
        self.setFixedSize(400, 300)


        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        left_container = QWidget()
        left_container.setObjectName("left_container")
        left_container.setFixedWidth(340)
        
        self.layout = QVBoxLayout(left_container)
        self.layout.setSpacing(30)
        self.layout.setContentsMargins(25, 25, 25, 25)
        
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        self.path_input.setMinimumHeight(45) 
        self.path_input.installEventFilter(self)
        input_layout.addWidget(self.path_input, 1, Qt.AlignmentFlag.AlignVCenter)
        
        self.btn_open = QPushButton()
        self.btn_open.setObjectName("btn_open")
        icon_path = os.path.join(os.path.dirname(__file__), 'folder_open.png')
        if os.path.exists(icon_path):
             self.btn_open.setIcon(QIcon(icon_path))
        self.btn_open.setIconSize(QSize(20, 20))
        self.btn_open.setFixedSize(45, 45)
        self.btn_open.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_open.clicked.connect(self.select_folder)
        input_layout.addWidget(self.btn_open, 10, Qt.AlignmentFlag.AlignVCenter)

        self.layout.addLayout(input_layout)
        
        # --- Action Buttons Section ---
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)

        self.btn_sort = QPushButton()
        self.btn_sort.setObjectName("btn_sort")
        self.btn_sort.setMinimumHeight(45)
        self.btn_sort.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_sort.clicked.connect(self.sort_files)
        action_layout.addWidget(self.btn_sort)
        
        self.btn_revert = QPushButton()
        self.btn_revert.setObjectName("btn_revert")
        self.btn_revert.setMinimumHeight(45)
        self.btn_revert.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_revert.clicked.connect(self.revert_files)
        action_layout.addWidget(self.btn_revert)

        self.layout.addLayout(action_layout)

        # --- Menu Bar for Language Selection ---
        self.create_menu_bar()

        main_layout.addWidget(left_container)
        
        copyright_label = QLabel("(C) - 2025 - VISALP")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_label.setStyleSheet("color: #888888; font-size: 10px; margin-top: 5px;")
        main_layout.addWidget(copyright_label)
        
        self.update_ui_texts()

    def create_menu_bar(self):
        menu_bar = QMenuBar(self) 
        
        lang_menu = menu_bar.addMenu("Language")
        
        lang_group = QActionGroup(self)
        lang_group.setExclusive(True)
        
        self.act_en = QAction("English - US", self)
        self.act_en.setCheckable(True)
        self.act_en.triggered.connect(lambda: self.change_language('en'))
        lang_menu.addAction(self.act_en)
        lang_group.addAction(self.act_en)
        
        self.act_hu = QAction("Hungarian - HU", self)
        self.act_hu.setCheckable(True)
        self.act_hu.triggered.connect(lambda: self.change_language('hu'))
        lang_menu.addAction(self.act_hu)
        lang_group.addAction(self.act_hu)
        
        if self.current_language == 'en':
            self.act_en.setChecked(True)
        else:
            self.act_hu.setChecked(True)

    def eventFilter(self, source, event):
        if source is self.path_input and event.type() == QEvent.Type.MouseButtonPress:
            self.select_folder()
            return True
        return super().eventFilter(source, event)

    def change_language(self, lang):
        self.current_language = lang
        self.update_ui_texts()
        
        if lang == 'en':
            self.act_en.setChecked(True)
        else:
            self.act_hu.setChecked(True)

    def update_ui_texts(self):
        lang_texts = self.translations[self.current_language]
        self.path_input.setPlaceholderText(lang_texts['placeholder_text'])
        self.btn_sort.setText(lang_texts['sort_btn'])
        self.btn_revert.setText(lang_texts['revert_btn'])

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(None, "Válassz mappát", "", QFileDialog.Option.ShowDirsOnly)
        if folder: self.path_input.setText(folder)

    def sort_files(self):
        source_dir = self.path_input.text()
        lang_texts = self.translations[self.current_language]

        if not source_dir or not os.path.isdir(source_dir):
            QMessageBox.warning(self, "Error", "Please select a valid directory first.")
            return

        reply = QMessageBox.question(self, lang_texts['confirm_title'], 
                                     lang_texts['confirm_sort'],
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.No:
            return

        translated_folder_names = self.translations[self.current_language]['folder_names']
        
        extension_to_folder = {}
        for category, extensions in self.FILE_CATEGORIES.items():
            folder_name = translated_folder_names[category]
            for ext in extensions:
                extension_to_folder[ext] = folder_name

        try:
            files_in_source_dir = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
        except FileNotFoundError:
             QMessageBox.warning(self, "Error", f"The directory {source_dir} was not found.")
             return

        moved_count = 0
        for filename in files_in_source_dir:
            _, ext = os.path.splitext(filename)
            dest_dir_name = extension_to_folder.get(ext.lower())

            if dest_dir_name:
                dest_dir = os.path.join(source_dir, dest_dir_name)
                
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                
                source_path = os.path.join(source_dir, filename)
                try:
                    shutil.move(source_path, os.path.join(dest_dir, filename))
                    moved_count += 1
                except Exception as e:
                    print(f"Error moving {filename}: {e}")
        
        QMessageBox.information(self, "Done", f"Sorting complete. Moved {moved_count} files.")


    def revert_files(self):
        source_dir = self.path_input.text()
        lang_texts = self.translations[self.current_language]

        if not source_dir or not os.path.isdir(source_dir):
             QMessageBox.warning(self, "Error", "Please select a valid directory first.")
             return

        reply = QMessageBox.question(self, lang_texts['confirm_title'], 
                                     lang_texts['confirm_revert'],
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.No:
            return

        all_folder_names = set()
        for lang_data in self.translations.values():
            all_folder_names.update(lang_data['folder_names'].values())

        reverted_count = 0
        for dir_name in all_folder_names:
            sub_dir = os.path.join(source_dir, dir_name)
            if os.path.isdir(sub_dir):
                for filename in os.listdir(sub_dir):
                    source_path = os.path.join(sub_dir, filename)
                    dest_path = os.path.join(source_dir, filename)
                    try:
                        shutil.move(source_path, dest_path)
                        reverted_count += 1
                    except Exception as e:
                         print(f"Error reverting {filename}: {e}")

                if not os.listdir(sub_dir):
                    try:
                        os.rmdir(sub_dir)
                    except OSError:
                        pass 
        
        QMessageBox.information(self, "Done", f"Revert complete. Moved back {reverted_count} files.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    ex = FileSorter()
    ex.show()
    sys.exit(app.exec())