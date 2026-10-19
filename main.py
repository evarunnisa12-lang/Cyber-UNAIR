import json
import os
import random

import flet as ft

NAVY = "#002b5c"
GOLD = "#d4af37"
BG = "#f4f6f9"

# =============================================================== PENGATURAN
SEMESTER_AKTIF = 5
TAHUN_MASUK = 2024          # Semester 1 = 2024/2025 Ganjil
KRS_DEADLINE = "19-08-2026"
KRS_DITUTUP = False         # True = KRS terkunci (checkbox tidak bisa diubah)
KPRS_DITUTUP = True
KODE_VERIFIKASI = "888999"  # kode simulasi SMS untuk membuka KHS
JUMLAH_PERTEMUAN = 14
BATAS_HADIR = 75            # persen kehadiran minimal

# Skor ELPT per bagian (total dihitung otomatis: rata-rata x 10)
ELPT_SKOR = {
    "Listening Comprehension": 53,
    "Structure & Written Expression": 52,
    "Reading Comprehension": 53,
}

# Jatah SKS maksimal yang disarankan berdasarkan IPS semester lalu
ATURAN_JATAH = [(3.00, 24), (2.50, 21), (2.00, 18), (1.50, 15), (0.00, 12)]

# ===================================================================== DATA
MAHASISWA = [
    ("182241001", "Salsabila Ramadhani Putri Riadi"),
    ("182241002", "Astri Dwi Pratiwi"),
    ("182241003", "Naela Halimatus Sa'diyah"),
    ("182241004", "Muhammad Zaki Farishul Haq"),
    ("182241005", "Lailatul Mufidah"),
    ("182241006", "Ahmad Najib Zaki"),
    ("182241007", "Rahel Tasyana Tambunan"),
    ("182241008", "Ahmad Ihfan Khoiri Habib"),
    ("182241009", "Sarah Hafidhah"),
    ("182241010", "Naila Zhafira Qurrotu 'Aini"),
    ("182241011", "Riska Elvina Putri Muslimah"),
    ("182241012", "Aisah"),
    ("182241013", "Neisya Salsabila Nasywa Fuad"),
    ("182241014", "Pradithya Putra Galang Islami"),
    ("182241015", "Naufal Lutfian Hakim"),
    ("182241017", "Salsabila Aliyah Wirawan"),
    ("182241018", "Hamidah Hasan"),
    ("182241019", "Nayla Izzati"),
    ("182241020", "Muhammad Febry Rahardian"),
    ("182241022", "Fifi Wardani"),
    ("182241023", "Abdurrahman Rafif"),
    ("182241024", "M. Farhan Fauzan"),
    ("182241025", "Dwi Safaatin"),
    ("182241026", "Gita Fajriyatin Puspa Rinjani"),
    ("182241027", "Alvin Firdausy"),
    ("182241028", "Jonatan Aditia Sihombing"),
    ("182241029", "Zuanida Indri Agustin"),
    ("182241030", "Diajeng Putri Imaya"),
    ("182241031", "Tiana Afiska Gianta Putri"),
    ("182241032", "Nabilah Wiedama Putri"),
    ("182241033", "Nanda Dwi Alfikri"),
    ("182241034", "Rijal Hadhari"),
    ("182241036", "Muhammad Abiyu Khansa"),
    ("182241037", "Lubaabindra M. Dzakwan"),
    ("182241038", "Dina Renanti Sitompul"),
    ("182241039", "Adelia Dwi Yuanita"),
    ("182241040", "Farras Atha Pandita"),
    ("182241041", "Tenia Cestri Azmiyanti"),
    ("182241042", "Ilham Putra Yuliawan"),
    ("182241043", "Hendra Maulana"),
    ("182241045", "Airin Khairunnisa Nur Raerah"),
    ("182241046", "Thomas Aquino Brilliant Aryawardhana"),
    ("182241047", "Pinkan Anjelita Isnamartandya"),
    ("182241048", "Aufa Dhiya Murtadlo"),
    ("182241049", "Mayta Rahmawati"),
    ("182241050", "Muhammad Nawvall Arya Tedy Herwanto"),
    ("182241051", "Putri Balqish Prita Aulia"),
    ("182241052", "Caroline Putri Kadri"),
    ("182241053", "Alexandria Putri Indriani Tutuko"),
    ("182241054", "Mohammad Akhsan Zaaky"),
    ("182241055", "Eva Khoirun Nisa"),
    ("182241056", "Moh. Nazril Ilham Adzani"),
    ("182241057", "Jazila Assafar Aswatul Mukaromah"),
    ("182241058", "Keyro Trisna Nugraha"),
    ("182241059", "Biema Mahawijaya Nawasetya"),
    ("182241060", "Gandani Putri Lunagustama"),
    ("182241062", "Dea Ayu Kisstia"),
]

DOSEN = {
    "FR": ("Febdian", "197902062008011004"),
    "NU": ("Nuril", "197004141999032001"),
    "AZ": ("Zaidan", "198304222006041001"),
    "IS": ("Imam", "197201181999031001"),
    "JA": ("Jan Ady", "197201262002121002"),
    "YG": ("Yhosep", "197309042006041001"),
    "Am": ("Aminatun", "196810281993032003"),
    "Wn": ("Winarno", "198109122015041001"),
    "DH": ("Dyah", "196911281994032001"),
    "SS": ("Soegi", "197001251993031003"),
    "DI": ("Djony Izak", "196802011993031004"),
    "EE": ("Edo", "198706042018083101"),
    "Sn": ("Samian", "196706211998021001"),
    "Sw": ("Siswanto", "196403051989031003"),
    "Pj": ("Puji", "196103251987101001"),
    "HT": ("Herri", "197712282003121003"),
    "RA": ("Retna", "196806261993032003"),
    "Si": ("Supadi", "197209181998021001"),
    "AS": ("Adri", "195603031986011002"),
    "SA": ("Suryani", "196908041994122001"),
    "SK": ("Septia", "199109062016113201"),
    "AD": ("Angga", "199205062020121012"),
}

# Kurikulum per semester: (nama mata kuliah, SKS awal)
# Semester 1-4 total 82 SKS (20 + 20 + 21 + 21).
# Pembagian semester & SKS ini perkiraan, bisa diubah di KRS > Ubah SKS.
KURIKULUM = {
    1: [
        ("Fisika Dasar", 3),
        ("Fisika Dasar (Praktikum)", 1),
        ("Fisika Matematika I", 3),
        ("Kalkulus I", 3),
        ("Kimia Dasar", 3),
        ("Kimia Dasar (Praktikum)", 1),
        ("Pancasila", 2),
        ("Bahasa Indonesia", 2),
        ("Pendidikan Agama", 2),
    ],  # 20 SKS
    2: [
        ("Fisika Dasar Lanjut", 3),
        ("Fisika Dasar Lanjut (Praktikum)", 1),
        ("Fisika Matematika II", 3),
        ("Fisika Gelombang", 3),
        ("Kalkulus II", 3),
        ("Aljabar Linear", 3),
        ("Bahasa Inggris", 2),
        ("Kewarganegaraan", 2),
    ],  # 20 SKS
    3: [
        ("Fisika Modern", 3),
        ("Termodinamika", 3),
        ("Elektronika I", 3),
        ("Elektronika I (Praktikum)", 1),
        ("Mekanika", 3),
        ("Mekanika (Praktikum)", 1),
        ("Biofisika", 2),
        ("Statistika", 3),
        ("Kewirausahaan", 2),
    ],  # 21 SKS
    4: [
        ("Fisika Kuantum", 3),
        ("Fisika Matematika III", 3),
        ("Fisika Eksperimental I", 2),
        ("Fisika Eksperimental I (Praktikum)", 1),
        ("Fisika Komputasi I", 2),
        ("Fisika Komputasi (Praktikum)", 1),
        ("Elektronika II", 3),
        ("Elektronika II (Praktikum)", 1),
        ("Metodologi Penelitian", 2),
        ("Bahasa Pemrograman", 3),
    ],  # 21 SKS
    5: [
        ("Fisika Atomik dan Molekuler", 3),
        ("Fisika Eksperimental II (Praktikum)", 1),
        ("Fisika Komputasi II", 2),
        ("Fisika Komputasi II (Praktikum)", 1),
        ("Fisika Statistik", 3),
        ("Listrik dan Magnet", 3),
        ("Listrik dan Magnet (Praktikum)", 1),
        ("Sensor dan Pengukuran", 3),
        ("Sistem Pengaturan", 3),
    ],
}

SKS_DEFAULT = {mk: s for mks in KURIKULUM.values() for mk, s in mks}
MATA_KULIAH = list(SKS_DEFAULT.keys())

KBK_LIST = [
    "Komputasi dan Sistem Cerdas",
    "Instrumentasi dan Energi",
    "Biofisika dan Fisika Medis",
    "Fisika Material",
    "Optika dan Aplikasi Laser",
    "Fisika Teoritis dan Rekayasa Kuantum Fisika",
]

BUKU_LIST = [
    "Fisika Atomik dan Molekuler - Bernhardt",
    "Fisika Eksperimental Lanjutan - Melissinos",
    "Fisika Komputasi II dengan Python - Pang",
    "Fisika Statistik dan Termodinamika - Reif",
    "Listrik dan Magnet - Purcell",
    "Sensor dan Pengukuran Industri - Doebelin",
    "Sistem Pengaturan (Control Systems Engineering) - Nise",
    "Fisika Matematika I, II, III - Arfken",
    "Mekanika Klasik - Goldstein",
    "Fisika Kuantum - Sakurai",
]
MAKS_PINJAM = 3

PROFILE_DEFAULT = {
    "fakultas": "Sains dan Teknologi (FST)",
    "prodi": "Fisika",
    "semester": "5",
    "dosen_wali": "Supadi, S.Si., M.Si.",
    "gender": "Perempuan",
    "kewarganegaraan": "WNI",
    "tgl_lahir": "16 Januari 2006",
    "hp": "081217756636",
    "agama": "Islam",
    "email": "evarunnisa12@gmail.com",
    "tahun_lulus": "2024",
}

BOBOT = {"A": 4.0, "AB": 3.5, "B": 3.0, "BC": 2.5, "C": 2.0, "D": 1.0, "E": 0.0}
WARNA_HURUF = {
    "A": "#15803d", "AB": "#15803d", "B": "#2563eb", "BC": "#2563eb",
    "C": "#d97706", "D": "#b91c1c", "E": "#b91c1c", "-": "#64748b",
}
KOSONG = {"tugas": "-", "uts": "-", "uas": "-", "akhir": "-", "huruf": "-"}

DATA_DIR = os.getenv("FLET_APP_STORAGE_DATA", os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(DATA_DIR, "cybercampus_data.json")


# ================================================================== HELPERS
def hitung_huruf(n):
    if n >= 85:
        return "A"
    if n >= 75:
        return "AB"
    if n >= 70:
        return "B"
    if n >= 65:
        return "BC"
    if n >= 60:
        return "C"
    if n >= 50:
        return "D"
    return "E"


def tahun_ajar(sem):
    mulai = TAHUN_MASUK + (sem - 1) // 2
    return f"{mulai}/{mulai + 1} {'Ganjil' if sem % 2 else 'Genap'}"


def jatah_dari_ips(ips):
    if ips is None:
        return 24
    for batas, sks in ATURAN_JATAH:
        if ips >= batas:
            return sks
    return ATURAN_JATAH[-1][1]


def fmt_ip(v):
    return f"{v:.2f}" if v is not None else "-"


def default_nilai():
    """Semester sebelum semester aktif diisi nilai contoh (deterministik)."""
    data = {}
    for nim, _nama in MAHASISWA:
        data[nim] = {}
        for sem, mks in KURIKULUM.items():
            for mk, _sks in mks:
                if sem < SEMESTER_AKTIF:
                    r = random.Random(f"{nim}|{mk}")
                    a = float(r.choice([92, 88, 86, 82, 78, 76, 72]))
                    data[nim][mk] = {
                        "tugas": str(a), "uts": str(a), "uas": str(a),
                        "akhir": str(a), "huruf": hitung_huruf(a),
                    }
                else:
                    data[nim][mk] = dict(KOSONG)
    return data


def load_db():
    db = {
        "nilai": default_nilai(),
        "sks": dict(SKS_DEFAULT),
        "krs": {},
        "kbk": {},
        "pinjam": {},
        "profile": dict(PROFILE_DEFAULT),
        "bobot": {"tugas": 30.0, "uts": 35.0, "uas": 35.0},
        "max_sks": 24,
    }
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            saved = json.load(f)
        for nim, mks in saved.get("nilai", {}).items():
            if nim in db["nilai"]:
                for mk, val in mks.items():
                    if mk in db["nilai"][nim]:
                        db["nilai"][nim][mk] = val
        for mk, v in saved.get("sks", {}).items():
            if mk in db["sks"]:
                db["sks"][mk] = int(v)
        for k in ("krs", "kbk", "pinjam"):
            db[k] = saved.get(k, {})
        db["profile"].update(saved.get("profile", {}))
        db["bobot"].update(saved.get("bobot", {}))
        db["max_sks"] = int(saved.get("max_sks", 24))
    except Exception:
        pass
    return db


def save_db(db):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False)
    except Exception:
        pass


def banner(text):
    return ft.Container(
        content=ft.Text(text, color="white", weight="bold", size=13),
        bgcolor=NAVY,
        padding=ft.padding.symmetric(horizontal=14, vertical=10),
        border_radius=6,
    )


def stat_card(label, val, besar=False):
    return ft.Container(
        bgcolor="#e2e8f0", border_radius=8, expand=True,
        padding=16 if besar else 10,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2,
            controls=[
                ft.Text(str(val), size=26 if besar else 18, weight="bold", color=NAVY),
                ft.Text(label, size=12 if besar else 10, color="#334155",
                        text_align="center"),
            ],
        ),
    )


def info_card(text, bg, fg, size=13):
    return ft.Container(
        bgcolor=bg, padding=14, border_radius=8,
        content=ft.Text(text, color=fg, weight="bold", size=size),
    )


def white_card(controls, spacing=8, padding=16):
    return ft.Container(
        bgcolor="white", padding=padding, border_radius=8,
        border=ft.border.all(1, "#e2e8f0"),
        content=ft.Column(controls, spacing=spacing),
    )


def make_pills(items, on_select, initial):
    """Tombol menu horizontal yang bisa digeser (pas untuk layar HP)."""
    pills = {}

    def paint(active):
        for n, c in pills.items():
            c.bgcolor = NAVY if n == active else "#e2e8f0"
            c.content.color = "white" if n == active else NAVY

    def select(name):
        paint(name)
        on_select(name)

    for n in items:
        pills[n] = ft.Container(
            data=n,
            on_click=lambda e: select(e.control.data),
            border_radius=16,
            padding=ft.padding.symmetric(horizontal=14, vertical=8),
            content=ft.Text(n, size=12, weight="bold"),
        )
    paint(initial)
    return ft.Row(list(pills.values()), scroll=ft.ScrollMode.AUTO, spacing=6)


# ====================================================================== MAIN
def main(page: ft.Page):
    page.title = "Cyber Campus - Universitas Airlangga"
    page.bgcolor = BG
    page.padding = 0

    db = load_db()
    state = {"captcha": "", "khs_ok": False}

    def toast(msg, error=False):
        page.open(ft.SnackBar(ft.Text(msg), bgcolor="#b91c1c" if error else "#15803d"))

    def nama_mhs(nim):
        return next((n for i, n in MAHASISWA if i == nim), nim)

    # ---- perhitungan akademik
    def stat_sem(nim, sem):
        """(IPS, SKS yang sudah dinilai) untuk satu semester."""
        tot = mutu = 0
        for mk, _ in KURIKULUM[sem]:
            h = db["nilai"][nim][mk]["huruf"]
            if h in BOBOT:
                s = db["sks"][mk]
                tot += s
                mutu += BOBOT[h] * s
        return (mutu / tot if tot else None), tot

    def stat_kumulatif(nim):
        """(IPK, total SKS diambil/dinilai, SKS lulus)."""
        tot = mutu = lulus = 0
        for sem in KURIKULUM:
            for mk, _ in KURIKULUM[sem]:
                h = db["nilai"][nim][mk]["huruf"]
                if h in BOBOT:
                    s = db["sks"][mk]
                    tot += s
                    mutu += BOBOT[h] * s
                    if BOBOT[h] >= 2.0:
                        lulus += s
        return (mutu / tot if tot else None), tot, lulus

    def sks_krs(nim):
        mk5 = [m for m, _ in KURIKULUM[SEMESTER_AKTIF]]
        pilih = db["krs"].get(nim, mk5)
        return sum(db["sks"][m] for m in pilih if m in db["sks"])

    def ipk_hingga(nim, s):
        """IPK kumulatif dari semester 1 sampai semester s."""
        tot = mutu = 0
        for sem in range(1, s + 1):
            for mk, _ in KURIKULUM[sem]:
                h = db["nilai"][nim][mk]["huruf"]
                if h in BOBOT:
                    sks = db["sks"][mk]
                    tot += sks
                    mutu += BOBOT[h] * sks
        return mutu / tot if tot else None

    def grafik_ip(nim):
        """Grafik batang IPS & IPK untuk semester yang sudah selesai (1-4)."""
        tinggi = 140
        kolom = []

        def bar(v, warna):
            return ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2,
                controls=[
                    ft.Text(fmt_ip(v), size=9, weight="bold", color=warna),
                    ft.Container(
                        width=22, height=max(2, (v or 0) / 4 * tinggi), bgcolor=warna,
                        border_radius=ft.border_radius.only(top_left=4, top_right=4)),
                ],
            )

        for sem in range(1, SEMESTER_AKTIF):
            ips, _ = stat_sem(nim, sem)
            ipk = ipk_hingga(nim, sem)
            kolom.append(
                ft.Column(
                    expand=True, spacing=4,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            height=tinggi + 20, spacing=6,
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            controls=[bar(ips, NAVY), bar(ipk, GOLD)]),
                        ft.Text(f"Sem {sem}", size=11, weight="bold"),
                    ],
                )
            )

        def legenda(warna, teks):
            return ft.Row([
                ft.Container(width=12, height=12, bgcolor=warna, border_radius=3),
                ft.Text(teks, size=11),
            ], spacing=4)

        return white_card([
            ft.Text("Grafik IPS & IPK per Semester (skala 0 - 4.00)",
                    weight="bold", color=NAVY, size=13),
            ft.Row(kolom, vertical_alignment=ft.CrossAxisAlignment.END),
            ft.Row([legenda(NAVY, "IPS"), legenda(GOLD, "IPK kumulatif")],
                   alignment=ft.MainAxisAlignment.CENTER, spacing=16),
        ], spacing=8)

    # ------------------------------------------------------------------ LOGIN
    def new_captcha():
        chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        state["captcha"] = "".join(random.choices(chars, k=5))

    def show_login():
        page.clean()
        new_captcha()

        entry_nim = ft.TextField(label="NIM Mahasiswa", value="182241055",
                                 keyboard_type=ft.KeyboardType.NUMBER)
        entry_pass = ft.TextField(label="Password", value="password123",
                                  password=True, can_reveal_password=True)
        entry_captcha = ft.TextField(label="Masukkan kode captcha")
        lbl_captcha = ft.Text(state["captcha"], size=24, weight="bold",
                              color="#0f172a", font_family="monospace")

        def refresh_cap(e=None):
            new_captcha()
            lbl_captcha.value = state["captcha"]
            entry_captcha.value = ""
            page.update()

        def verify(e):
            nim = (entry_nim.value or "").strip()
            pwd = (entry_pass.value or "").strip()
            cap = (entry_captcha.value or "").strip().upper()
            if not nim or not pwd or not cap:
                toast("Semua kolom harus diisi!", True)
                return
            if cap != state["captcha"]:
                toast("Kode Captcha salah!", True)
                refresh_cap()
                return
            if any(m[0] == nim for m in MAHASISWA):
                show_main(nim)
            else:
                toast("NIM tidak terdaftar di sistem Cyber Campus!", True)
                refresh_cap()

        card = ft.Container(
            width=380, bgcolor="white", border_radius=12, padding=24,
            content=ft.Column(
                tight=True, spacing=12,
                controls=[
                    ft.Text("CYBER CAMPUS", size=22, weight="bold", color=NAVY,
                            text_align="center"),
                    ft.Text("Universitas Airlangga", italic=True, color=GOLD,
                            text_align="center"),
                    entry_nim, entry_pass,
                    ft.Container(
                        bgcolor="#cbd5e1", border_radius=6, padding=8,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[lbl_captcha, ft.TextButton("Ganti", on_click=refresh_cap)],
                        ),
                    ),
                    entry_captcha,
                    ft.ElevatedButton("LOGIN", on_click=verify, bgcolor=NAVY,
                                      color="white", height=46, width=400),
                ],
            ),
        )
        page.add(
            ft.Container(
                expand=True, bgcolor=NAVY, alignment=ft.alignment.center, padding=16,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[card],
                ),
            )
        )
        page.update()

    # ============================================================== AKADEMIK
    def sub_krs(nim, rerender):
        mk5 = [m for m, _ in KURIKULUM[SEMESTER_AKTIF]]
        tersimpan = db["krs"].get(nim)
        terpilih = set(tersimpan if tersimpan is not None else mk5)

        slider = ft.Slider(min=12, max=24, divisions=12, value=db["max_sks"],
                           label="{value} SKS")
        lbl_jatah = ft.Text("", weight="bold", color=NAVY)
        lbl_total = ft.Text("", weight="bold", color=NAVY)
        ips_lalu, _ = stat_sem(nim, SEMESTER_AKTIF - 1)
        lbl_saran = ft.Text(
            f"Saran jatah dari IPS semester lalu ({fmt_ip(ips_lalu)}): "
            f"{jatah_dari_ips(ips_lalu)} SKS",
            size=11, color="#64748b")
        cbs = {}

        def total():
            return sum(db["sks"][m] for m in mk5 if cbs[m].value)

        def update_total():
            t = total()
            lbl_total.value = f"SKS dipilih: {t} / {db['max_sks']}"
            lbl_total.color = "#b91c1c" if t > db["max_sks"] else NAVY
            lbl_jatah.value = f"Jatah SKS maksimal saat ini: {db['max_sks']} SKS"
            page.update()

        def simpan_jatah(e):
            db["max_sks"] = int(slider.value)
            save_db(db)
            update_total()
            toast("Jatah SKS berhasil disimpan!")

        for mk in mk5:
            cbs[mk] = ft.Checkbox(
                label=f"{mk} ({db['sks'][mk]} SKS)",
                value=mk in terpilih,
                disabled=KRS_DITUTUP,
                on_change=lambda e: update_total(),
            )

        def pilih_semua(e):
            for c in cbs.values():
                c.value = True
            update_total()

        def kosongkan(e):
            for c in cbs.values():
                c.value = False
            update_total()

        def simpan_krs(e):
            t = total()
            if t == 0:
                toast("Pilih minimal satu mata kuliah!", True)
                return
            if t > db["max_sks"]:
                toast(f"Total SKS ({t}) melebihi jatah maksimal ({db['max_sks']} SKS)!", True)
                return
            db["krs"][nim] = [m for m in mk5 if cbs[m].value]
            save_db(db)
            toast(f"KRS tersimpan: {len(db['krs'][nim])} mata kuliah, {t} SKS.")

        # --- editor SKS per mata kuliah
        dd_sem = ft.Dropdown(
            label="Semester",
            value=str(SEMESTER_AKTIF),
            options=[ft.dropdown.Option(str(s), f"Semester {s}") for s in KURIKULUM],
        )
        sks_col = ft.Column(spacing=6)
        fields = {}

        def build_fields(e=None):
            fields.clear()
            sks_col.controls.clear()
            for mk, _ in KURIKULUM[int(dd_sem.value)]:
                fields[mk] = ft.TextField(value=str(db["sks"][mk]), width=70, dense=True,
                                          text_align="center",
                                          keyboard_type=ft.KeyboardType.NUMBER)
                sks_col.controls.append(
                    ft.Row([ft.Text(mk, expand=True, size=13), fields[mk]],
                           vertical_alignment=ft.CrossAxisAlignment.CENTER))
            page.update()

        def simpan_sks(e):
            baru = {}
            for mk, f in fields.items():
                try:
                    v = int((f.value or "").strip())
                except ValueError:
                    toast(f"SKS '{mk}' harus berupa angka bulat!", True)
                    return
                if not 1 <= v <= 6:
                    toast(f"SKS '{mk}' harus antara 1 dan 6!", True)
                    return
                baru[mk] = v
            db["sks"].update(baru)
            save_db(db)
            toast("SKS mata kuliah berhasil diperbarui!")
            rerender()

        def reset_sks(e):
            for mk in fields:
                db["sks"][mk] = SKS_DEFAULT[mk]
            save_db(db)
            toast("SKS dikembalikan ke nilai awal.")
            rerender()

        dd_sem.on_change = build_fields
        build_fields()
        update_total()

        if KRS_DITUTUP:
            status = info_card(
                f"Batas akhir pengisian KRS sudah ditutup pada tanggal {KRS_DEADLINE}.",
                "#fef3c7", "#92400e")
        else:
            status = info_card(
                f"Pengisian KRS dibuka. Batas akhir: {KRS_DEADLINE}.",
                "#dcfce7", "#166534")

        return ft.Column(
            [
                banner(f"PENGISIAN KARTU RENCANA STUDI (KRS) - SEMESTER {SEMESTER_AKTIF}"),
                status,
                white_card([
                    lbl_jatah,
                    lbl_saran,
                    ft.Text("Geser untuk mengubah batas maksimal jatah SKS:", size=12),
                    slider,
                    ft.ElevatedButton("Simpan Jatah SKS", on_click=simpan_jatah,
                                      bgcolor=NAVY, color="white"),
                ]),
                white_card([
                    ft.Text("Pilih mata kuliah yang diambil:", weight="bold", color=NAVY),
                    *cbs.values(),
                    lbl_total,
                    ft.Row([
                        ft.ElevatedButton("Simpan KRS", on_click=simpan_krs,
                                          bgcolor=NAVY, color="white",
                                          disabled=KRS_DITUTUP),
                        ft.TextButton("Pilih semua", on_click=pilih_semua,
                                      disabled=KRS_DITUTUP),
                        ft.TextButton("Kosongkan", on_click=kosongkan,
                                      disabled=KRS_DITUTUP),
                    ], wrap=True),
                ], spacing=2),
                ft.ExpansionTile(
                    title=ft.Text("Ubah SKS Mata Kuliah", weight="bold"),
                    bgcolor="white",
                    controls=[ft.Container(padding=12, content=ft.Column([
                        dd_sem, sks_col,
                        ft.Row([
                            ft.ElevatedButton("Simpan SKS", on_click=simpan_sks,
                                              bgcolor=NAVY, color="white"),
                            ft.TextButton("Reset ke awal", on_click=reset_sks),
                        ]),
                    ], spacing=8))],
                ),
            ],
            expand=True, spacing=10, scroll=ft.ScrollMode.AUTO,
        )

    def sub_khs(nim, rerender):
        txt_kode = ft.TextField(label="Masukkan Kode Verifikasi SMS",
                                keyboard_type=ft.KeyboardType.NUMBER)

        def do_verify(e):
            if (txt_kode.value or "").strip() == KODE_VERIFIKASI:
                state["khs_ok"] = True
                toast("Kode verifikasi benar!")
                rerender()
            else:
                toast(f"Kode verifikasi salah! (Simulasi kode: {KODE_VERIFIKASI})", True)

        if not state["khs_ok"]:
            return ft.Column(
                [
                    banner("KARTU HASIL STUDI (KHS)"),
                    white_card([
                        ft.Text("Verifikasi Keamanan KHS", weight="bold", color=NAVY, size=15),
                        ft.Text(
                            "Kode verifikasi telah dikirimkan melalui pesan SMS ke nomor "
                            f"telepon terhubung ({db['profile']['hp']}). "
                            f"(Simulasi kode: {KODE_VERIFIKASI})",
                            size=12, color="#475569"),
                        txt_kode,
                        ft.ElevatedButton("Verifikasi & Buka KHS", on_click=do_verify,
                                          bgcolor=NAVY, color="white"),
                    ], spacing=10, padding=20),
                ],
                expand=True, spacing=10, scroll=ft.ScrollMode.AUTO,
            )

        dd = ft.Dropdown(
            label="Pilih Semester",
            value=str(SEMESTER_AKTIF),
            options=[ft.dropdown.Option(str(s), f"Semester {s} - {tahun_ajar(s)}")
                     for s in KURIKULUM],
        )
        hasil = ft.Column(spacing=8)

        def render(e=None):
            sem = int(dd.value)
            ips, sks_n = stat_sem(nim, sem)
            ipk, _, lulus = stat_kumulatif(nim)
            sks_paket = sum(db["sks"][mk] for mk, _ in KURIKULUM[sem])
            hasil.controls = [
                ft.Row([stat_card("IPS", fmt_ip(ips)), stat_card("IPK", fmt_ip(ipk)),
                        stat_card("SKS Semester", sks_paket), stat_card("SKS Lulus", lulus)]),
            ]
            for mk, _ in KURIKULUM[sem]:
                v = db["nilai"][nim][mk]
                h = v["huruf"]
                bobot = f"{BOBOT[h]:.1f}" if h in BOBOT else "-"
                hasil.controls.append(
                    ft.Container(
                        bgcolor="white", border_radius=8, padding=10,
                        border=ft.border.all(1, "#e2e8f0"),
                        content=ft.Column([
                            ft.Text(mk, weight="bold", color=NAVY),
                            ft.Text(f"SKS: {db['sks'][mk]} | Tugas: {v['tugas']} | "
                                    f"UTS: {v['uts']} | UAS: {v['uas']}", size=11),
                            ft.Text(f"Nilai Akhir: {v['akhir']} | Huruf: {h} | Bobot: {bobot}",
                                    weight="bold", size=11, color=WARNA_HURUF[h]),
                        ], spacing=2),
                    )
                )
            page.update()

        dd.on_change = render
        render()
        return ft.Column(
            [banner("KARTU HASIL STUDI (KHS)"), dd, hasil],
            expand=True, spacing=10, scroll=ft.ScrollMode.AUTO,
        )

    def sub_kprs():
        if KPRS_DITUTUP:
            isi = info_card(
                "Maaf, KPRS sudah ditutup, silahkan hubungi bagian akademik prodi",
                "#fee2e2", "#991b1b", 14)
        else:
            isi = info_card("KPRS sedang dibuka.", "#dcfce7", "#166534", 14)
        return ft.Column([banner("KARTU PERUBAHAN RENCANA STUDI (KPRS)"), isi],
                         expand=True, spacing=10)

    def sub_histori(nim):
        ipk, tot, lulus = stat_kumulatif(nim)
        tiles = []
        for sem in sorted(KURIKULUM, reverse=True):
            ips, _ = stat_sem(nim, sem)
            rows = []
            for mk, _ in KURIKULUM[sem]:
                h = db["nilai"][nim][mk]["huruf"]
                bobot = f"Bobot {BOBOT[h]:.1f}" if h in BOBOT else "Belum dinilai"
                rows.append(
                    ft.Container(
                        bgcolor="white", padding=10, border_radius=6,
                        border=ft.border.all(1, "#e2e8f0"),
                        content=ft.Row([
                            ft.Column([
                                ft.Text(mk, weight="bold", size=12),
                                ft.Text(f"{db['sks'][mk]} SKS | {bobot}", size=10,
                                        color="#64748b"),
                            ], expand=True, spacing=2),
                            ft.Text(h, size=14, weight="bold", color=WARNA_HURUF[h]),
                        ]),
                    )
                )
            tiles.append(
                ft.ExpansionTile(
                    title=ft.Text(f"Semester {sem} - {tahun_ajar(sem)}", weight="bold",
                                  size=13),
                    subtitle=ft.Text(f"IPS: {fmt_ip(ips)}", size=11),
                    bgcolor="white",
                    initially_expanded=(sem == SEMESTER_AKTIF - 1),
                    controls=[ft.Container(padding=8, content=ft.Column(rows, spacing=6))],
                )
            )
        return ft.Column(
            [
                banner("HISTORI NILAI AKADEMIK MAHASISWA"),
                ft.Row([stat_card("IPK", fmt_ip(ipk), True),
                        stat_card("SKS Diambil", tot, True)]),
                ft.Row([stat_card("SKS Lulus", lulus, True),
                        stat_card("Jatah SKS", db["max_sks"], True)]),
                grafik_ip(nim),
                *tiles,
            ],
            expand=True, spacing=8, scroll=ft.ScrollMode.AUTO,
        )

    def sub_absen(nim):
        items = []
        for mk, _ in KURIKULUM[SEMESTER_AKTIF]:
            r = random.Random(f"{nim}|{mk}|absen")
            hadir = r.choice([14, 14, 13, 13, 12, 11])
            pct = hadir / JUMLAH_PERTEMUAN * 100
            if pct >= 90:
                warna, ket = "#15803d", "Aman"
            elif pct >= 85:
                warna, ket = "#2563eb", "Aman"
            else:
                warna, ket = "#d97706", "Aman - Perlu Perhatian"
            items.append(
                ft.Container(
                    bgcolor="white", padding=10, border_radius=6,
                    border=ft.border.all(1, "#cbd5e1"),
                    content=ft.Column([
                        ft.Row([
                            ft.Text(mk, weight="bold", size=12, expand=True),
                            ft.Text(f"{hadir}/{JUMLAH_PERTEMUAN} ({pct:.0f}%)",
                                    weight="bold", size=11, color=warna),
                        ]),
                        ft.ProgressBar(value=hadir / JUMLAH_PERTEMUAN, color=warna,
                                       bgcolor="#e2e8f0", height=6),
                        ft.Text(f"Status: {ket}", size=10, color=warna),
                    ], spacing=4),
                )
            )
        return ft.Column(
            [
                banner(f"REKAP ABSENSI PERKULIAHAN - SEMESTER {SEMESTER_AKTIF}"),
                ft.Text(f"Batas kehadiran minimal {BATAS_HADIR}%. "
                        "Seluruh mata kuliah berstatus aman (tidak ada pencekalan).",
                        size=11, italic=True),
                *items,
            ],
            expand=True, spacing=8, scroll=ft.ScrollMode.AUTO,
        )

    def sub_elpt():
        total = round(sum(ELPT_SKOR.values()) / len(ELPT_SKOR) * 10)
        return ft.Column(
            [
                banner("HASIL ENGLISH LANGUAGE PROFICIENCY TEST (ELPT)"),
                white_card([
                    ft.Text(f"Skor Total ELPT: {total}", weight="bold", size=18, color=NAVY),
                    ft.Divider(),
                    *[ft.ListTile(title=ft.Text(n), subtitle=ft.Text(f"Skor: {s}", weight="bold"))
                      for n, s in ELPT_SKOR.items()],
                ], spacing=4, padding=20),
            ],
            expand=True, spacing=10, scroll=ft.ScrollMode.AUTO,
        )

    def sub_wisuda():
        return ft.Column(
            [banner("STATUS PENGAJUAN WISUDA"),
             info_card("Anda belum Yudisium, Harap Hubungi Akademik Fakultas",
                       "#fef3c7", "#92400e", 14)],
            expand=True, spacing=10)

    def sub_kkn():
        return ft.Column(
            [banner("KULIAH KERJA NYATA (KKN)"),
             info_card("Anda tidak termasuk dalam peserta KKN pada angkatan BBK 9 Tahun 2027",
                       "#fee2e2", "#991b1b")],
            expand=True, spacing=10)

    def sub_minat(nim):
        chosen = list(db["kbk"].get(nim, []))
        daftar = ft.Column(spacing=8)
        lbl_status = ft.Text("", size=12, weight="bold", color=NAVY)

        def toggle(e):
            nama = e.control.data
            if nama in chosen:
                chosen.remove(nama)
            elif len(chosen) < 3:
                chosen.append(nama)
            else:
                toast("Maksimal 3 KBK. Lepas salah satu pilihan terlebih dahulu.", True)
            render()

        def render():
            daftar.controls.clear()
            for kbk in KBK_LIST:
                urutan = chosen.index(kbk) + 1 if kbk in chosen else None
                daftar.controls.append(
                    ft.Container(
                        bgcolor="#eff6ff" if urutan else "white", padding=12,
                        border_radius=8, data=kbk, on_click=toggle,
                        border=ft.border.all(1, NAVY if urutan else "#cbd5e1"),
                        content=ft.Row([
                            ft.Container(
                                width=26, height=26, border_radius=13,
                                bgcolor=NAVY if urutan else "white",
                                border=ft.border.all(2, NAVY),
                                alignment=ft.alignment.center,
                                content=ft.Text(str(urutan) if urutan else "", color="white",
                                                weight="bold", size=12),
                            ),
                            ft.Text(kbk, weight="bold", color=NAVY, size=13, expand=True),
                        ], spacing=12),
                    )
                )
            saved = db["kbk"].get(nim, [])
            lbl_status.value = (f"Dipilih: {len(chosen)}/3"
                                + ("  |  Tersimpan" if saved and saved == chosen else ""))
            page.update()

        def simpan(e):
            if len(chosen) != 3:
                toast(f"Pilih tepat 3 KBK (saat ini {len(chosen)})!", True)
                return
            db["kbk"][nim] = list(chosen)
            save_db(db)
            render()
            toast("Pilihan KBK berhasil disimpan!")

        def reset(e):
            chosen.clear()
            render()

        render()
        return ft.Column(
            [
                banner("PEMINATAN PROGRAM STUDI FISIKA (PILIH TEPAT 3 KBK)"),
                ft.Text("Ketuk untuk memilih. Angka menunjukkan urutan prioritas "
                        "(1 = paling diminati). Ketuk lagi untuk melepas.",
                        size=11, italic=True),
                daftar, lbl_status,
                ft.Row([
                    ft.ElevatedButton("Simpan Pilihan KBK", on_click=simpan,
                                      bgcolor=NAVY, color="white"),
                    ft.TextButton("Reset", on_click=reset),
                ]),
            ],
            expand=True, spacing=10, scroll=ft.ScrollMode.AUTO,
        )

    SUB_AKADEMIK = ["KRS", "KHS", "KPRS", "Histori Nilai", "Rekap Absen",
                    "ELPT", "Pengajuan Wisuda", "KKN", "Minat Prodi"]

    def menu_akademik(nim):
        box = ft.Container(expand=True)

        def bangun(name):
            def rerender():
                show(name)
            if name == "KRS":
                return sub_krs(nim, rerender)
            if name == "KHS":
                return sub_khs(nim, rerender)
            if name == "KPRS":
                return sub_kprs()
            if name == "Histori Nilai":
                return sub_histori(nim)
            if name == "Rekap Absen":
                return sub_absen(nim)
            if name == "ELPT":
                return sub_elpt()
            if name == "Pengajuan Wisuda":
                return sub_wisuda()
            if name == "KKN":
                return sub_kkn()
            return sub_minat(nim)

        def show(name):
            box.content = bangun(name)
            page.update()

        pills = make_pills(SUB_AKADEMIK, show, "KHS")
        box.content = bangun("KHS")
        return ft.Column(
            [banner("NAVIGASI AKADEMIK MAHASISWA"), pills, box],
            expand=True, spacing=10,
        )

    # ================================================================== DOSEN
    def dosen_penilaian():
        sel = {"nim": None}
        mk5 = [m for m, _ in KURIKULUM[SEMESTER_AKTIF]]
        b = db["bobot"]

        dd_dosen = ft.Dropdown(
            label="Pilih Dosen Pengajar", value="FR",
            options=[ft.dropdown.Option(key=k, text=f"[{k}] {v[0]} - NIP. {v[1]}")
                     for k, v in DOSEN.items()],
        )
        dd_mk = ft.Dropdown(
            label=f"Mata Kuliah Semester {SEMESTER_AKTIF}", value=mk5[0],
            options=[ft.dropdown.Option(m) for m in mk5],
        )
        lbl_sel = ft.Text("Belum ada mahasiswa dipilih", weight="bold", color=NAVY)
        f_tugas = ft.TextField(label=f"Tugas ({b['tugas']:g}%)", expand=True,
                               keyboard_type=ft.KeyboardType.NUMBER)
        f_uts = ft.TextField(label=f"UTS ({b['uts']:g}%)", expand=True,
                             keyboard_type=ft.KeyboardType.NUMBER)
        f_uas = ft.TextField(label=f"UAS ({b['uas']:g}%)", expand=True,
                             keyboard_type=ft.KeyboardType.NUMBER)
        lv = ft.ListView(expand=True, spacing=4)

        def refresh():
            lv.controls.clear()
            mk = dd_mk.value
            for idx, (nim, nama) in enumerate(MAHASISWA, 1):
                v = db["nilai"][nim][mk]
                lv.controls.append(
                    ft.Container(
                        data=nim, on_click=pilih,
                        bgcolor="#dbeafe" if sel["nim"] == nim else "white",
                        border_radius=6, padding=8,
                        content=ft.Column(spacing=2, controls=[
                            ft.Text(f"{idx}. {nama}", weight="bold", size=12),
                            ft.Text(f"NIM {nim} | T:{v['tugas']} UTS:{v['uts']} "
                                    f"UAS:{v['uas']} Akhir:{v['akhir']} ({v['huruf']})",
                                    size=10, color="#475569"),
                        ]),
                    )
                )
            page.update()

        def pilih(e):
            sel["nim"] = e.control.data
            lbl_sel.value = f"Dipilih: {sel['nim']} - {nama_mhs(sel['nim'])}"
            refresh()

        def simpan(e):
            if not sel["nim"]:
                toast("Pilih mahasiswa terlebih dahulu!", True)
                return
            try:
                t = float(f_tugas.value) if f_tugas.value else 0.0
                u = float(f_uts.value) if f_uts.value else 0.0
                s = float(f_uas.value) if f_uas.value else 0.0
            except ValueError:
                toast("Nilai harus berupa angka!", True)
                return
            if not (0 <= t <= 100 and 0 <= u <= 100 and 0 <= s <= 100):
                toast("Setiap nilai harus berada di antara 0 dan 100!", True)
                return
            akhir = round((b["tugas"] * t + b["uts"] * u + b["uas"] * s) / 100, 2)
            db["nilai"][sel["nim"]][dd_mk.value] = {
                "tugas": str(t), "uts": str(u), "uas": str(s),
                "akhir": str(akhir), "huruf": hitung_huruf(akhir),
            }
            save_db(db)
            f_tugas.value = f_uts.value = f_uas.value = ""
            refresh()
            toast("Nilai berhasil disimpan!")

        dd_mk.on_change = lambda e: refresh()
        refresh()
        return ft.Column(
            [
                dd_dosen, dd_mk,
                banner("PANEL DOSEN: INPUT PENILAIAN"),
                lv,
                ft.Container(
                    bgcolor="#f8fafc", border_radius=6, padding=10,
                    border=ft.border.all(1, "#cbd5e1"),
                    content=ft.Column([
                        lbl_sel,
                        ft.Row([f_tugas, f_uts, f_uas]),
                        ft.ElevatedButton("Simpan & Hitung Nilai", on_click=simpan,
                                          bgcolor=NAVY, color="white"),
                    ], tight=True),
                ),
            ],
            expand=True, spacing=8,
        )

    def dosen_komponen():
        mk5 = [m for m, _ in KURIKULUM[SEMESTER_AKTIF]]
        dd_mk = ft.Dropdown(label="Mata Kuliah", value=mk5[0],
                            options=[ft.dropdown.Option(m) for m in mk5])
        lbl = ft.Text("", weight="bold", color=NAVY, size=12)
        lv = ft.ListView(expand=True, spacing=4)

        def render(e=None):
            mk = dd_mk.value
            cnt = {h: 0 for h in list(BOBOT) + ["-"]}
            lv.controls.clear()
            for idx, (nim, nama) in enumerate(MAHASISWA, 1):
                v = db["nilai"][nim][mk]
                cnt[v["huruf"]] += 1
                lv.controls.append(
                    ft.Container(
                        bgcolor="white", border_radius=6, padding=8,
                        content=ft.Row([
                            ft.Text(f"{idx}. {nama}", size=12, expand=True),
                            ft.Text(f"{v['akhir']} ({v['huruf']})", size=12, weight="bold",
                                    color=WARNA_HURUF[v["huruf"]]),
                        ]),
                    )
                )
            lbl.value = "Distribusi nilai: " + "  ".join(
                f"{h}:{c}" for h, c in cnt.items() if c)
            page.update()

        dd_mk.on_change = render
        render()
        return ft.Column([dd_mk, banner("REKAP KOMPONEN NILAI KELAS"), lbl, lv],
                         expand=True, spacing=8)

    def dosen_pengajaran():
        jadwal = [
            ("Fisika Atomik dan Molekuler", "Kelas 488 (Senin) & Kelas 489 (Rabu)",
             "FR (Febdian) [PJMK]", "GC-4.06"),
            ("Fisika Komputasi II", "Kelas 488 (Selasa) & Kelas 489 (Kamis)",
             "NU (Nuril) [PJMK]", "GC-4.05"),
            ("Fisika Statistik", "Kelas 488 (Senin) & Kelas 489 (Rabu)",
             "Sn (Samian) [PJMK]", "GC-4.06"),
            ("Listrik dan Magnet", "Kelas 488 (Senin) & Kelas 489 (Jumat)",
             "DH (Dyah) [PJMK]", "GC-4.05"),
            ("Sensor dan Pengukuran", "Kelas 2 (Rabu)", "YG (Yhosep)", "GC-4.04"),
        ]
        lv = ft.ListView(expand=True, spacing=6)
        for mk, waktu, dsn, ruang in jadwal:
            lv.controls.append(
                ft.Container(
                    bgcolor="white", padding=12, border_radius=6,
                    border=ft.border.all(1, "#cbd5e1"),
                    content=ft.Column([
                        ft.Text(mk, weight="bold", color=NAVY),
                        ft.Text(f"Jadwal: {waktu}", size=11),
                        ft.Text(f"Dosen Pengampu / PJMK: {dsn}", size=11, weight="bold",
                                color="#15803d"),
                        ft.Text(f"Ruang: {ruang}", size=11),
                    ], spacing=2),
                )
            )
        return ft.Column(
            [banner(f"JADWAL PENGAJARAN DOSEN - SEMESTER {SEMESTER_AKTIF}"), lv],
            expand=True, spacing=8)

    def dosen_bimbingan():
        return ft.Column(
            [banner("MANAJEMEN BIMBINGAN AKADEMIK & TUGAS AKHIR"),
             white_card([
                 ft.Text("Daftar Mahasiswa Bimbingan Wali:", weight="bold"),
                 ft.ListTile(title=ft.Text("Eva Khoirun Nisa (182241055)"),
                             subtitle=ft.Text("Status Bimbingan: Aktif | Topik: Fisika Komputasi")),
                 ft.ListTile(title=ft.Text("Salsabila Ramadhani (182241001)"),
                             subtitle=ft.Text("Status Bimbingan: Aktif | Topik: Instrumentasi")),
             ], spacing=4, padding=20)],
            expand=True, spacing=10, scroll=ft.ScrollMode.AUTO)

    def dosen_kkn():
        return ft.Column(
            [banner("KONTROL & MONITORING KKN MAHASISWA"),
             white_card([
                 ft.Text("Monitoring Lokasi & Kelompok KKN-BBK:", weight="bold"),
                 ft.Text("• Lokasi Penempatan: Kabupaten Lamongan", size=12),
                 ft.Text("• Dosen Pembimbing Lapangan (DPL): Dr. Febdian Rusydi, S.Si., M.Sc.",
                         size=12),
                 ft.Text("• Status Laporan Kegiatan: Terverifikasi", size=12,
                         color="#15803d", weight="bold"),
             ], spacing=6, padding=20)],
            expand=True, spacing=10, scroll=ft.ScrollMode.AUTO)

    def dosen_setting(rerender):
        b = db["bobot"]
        f_t = ft.TextField(label="Bobot Tugas (%)", value=f"{b['tugas']:g}",
                           keyboard_type=ft.KeyboardType.NUMBER)
        f_u = ft.TextField(label="Bobot UTS (%)", value=f"{b['uts']:g}",
                           keyboard_type=ft.KeyboardType.NUMBER)
        f_s = ft.TextField(label="Bobot UAS (%)", value=f"{b['uas']:g}",
                           keyboard_type=ft.KeyboardType.NUMBER)

        def simpan(e):
            try:
                t, u, s = float(f_t.value), float(f_u.value), float(f_s.value)
            except (TypeError, ValueError):
                toast("Bobot harus berupa angka!", True)
                return
            if min(t, u, s) < 0 or abs(t + u + s - 100) > 0.001:
                toast(f"Total bobot harus 100% (saat ini {t + u + s:g}%)!", True)
                return
            db["bobot"] = {"tugas": t, "uts": u, "uas": s}
            save_db(db)
            toast("Bobot penilaian diperbarui!")

        return ft.Column(
            [banner("PENGATURAN KOMPONEN BOBOT PENILAIAN"),
             white_card([
                 f_t, f_u, f_s,
                 ft.Text("Total bobot harus 100%. Berlaku untuk perhitungan nilai berikutnya.",
                         size=11, color="#64748b"),
                 ft.ElevatedButton("Simpan Konfigurasi Bobot", on_click=simpan,
                                   bgcolor=NAVY, color="white"),
             ], spacing=10, padding=20)],
            expand=True, spacing=10, scroll=ft.ScrollMode.AUTO)

    SUB_DOSEN = ["Pengajaran", "Penilaian", "Komponen Nilai", "Bimbingan",
                 "Kontrol KKN", "Setting Penilaian"]

    def menu_dosen():
        box = ft.Container(expand=True)

        def bangun(name):
            if name == "Pengajaran":
                return dosen_pengajaran()
            if name == "Penilaian":
                return dosen_penilaian()
            if name == "Komponen Nilai":
                return dosen_komponen()
            if name == "Bimbingan":
                return dosen_bimbingan()
            if name == "Kontrol KKN":
                return dosen_kkn()
            return dosen_setting(lambda: None)

        def show(name):
            box.content = bangun(name)
            page.update()

        pills = make_pills(SUB_DOSEN, show, "Pengajaran")
        box.content = bangun("Pengajaran")
        return ft.Column([pills, box], expand=True, spacing=10)

    # ================================================================ MENU LAIN
    def menu_home(nim):
        ipk, tot, lulus = stat_kumulatif(nim)
        krs_txt = ("sudah ditutup pada tanggal " if KRS_DITUTUP
                   else "dibuka, batas akhir ") + KRS_DEADLINE
        return ft.Column(
            [
                banner("BERANDA UTAMA CYBER CAMPUS"),
                white_card([
                    ft.Text(f"Selamat Datang, {nama_mhs(nim)}", size=18, weight="bold",
                            color=NAVY),
                    ft.Text(f"NIM: {nim} | Program Studi: {db['profile']['prodi']} | "
                            f"Semester: {SEMESTER_AKTIF}", size=13, color="#475569"),
                ], spacing=6, padding=20),
                ft.Row([stat_card("IPK", fmt_ip(ipk), True),
                        stat_card("SKS Diambil", tot, True)]),
                ft.Row([stat_card("SKS Lulus", lulus, True),
                        stat_card("Jatah SKS", db["max_sks"], True)]),
                ft.Row([stat_card("SKS di KRS", sks_krs(nim), True)]),
                grafik_ip(nim),
                white_card([
                    ft.Text("Pengumuman Akademik Terbaru:", weight="bold"),
                    ft.Text(f"• Pengisian Kartu Rencana Studi (KRS) {krs_txt}.", size=12),
                    ft.Text("• Ujian Tengah Semester (UTS) sudah selesai dilakukan.", size=12),
                    ft.Text("• Jadwal Ujian Akhir Semester (UAS) akan diumumkan.", size=12),
                ], spacing=8, padding=20),
            ],
            expand=True, spacing=10, scroll=ft.ScrollMode.AUTO,
        )

    def menu_biodata(nim):
        p = db["profile"]
        t_hp = ft.TextField(label="Nomor Handphone", value=p["hp"])
        t_email = ft.TextField(label="Alamat Email", value=p["email"])
        t_agama = ft.TextField(label="Agama", value=p["agama"])
        t_tgl = ft.TextField(label="Tanggal Lahir", value=p["tgl_lahir"])

        def save_bio(e):
            p["hp"], p["email"] = t_hp.value, t_email.value
            p["agama"], p["tgl_lahir"] = t_agama.value, t_tgl.value
            save_db(db)
            toast("Biodata berhasil diperbarui!")

        def baris(label, val):
            return ft.Row([
                ft.Text(label, size=12, color="#64748b", width=120),
                ft.Text(val, size=13, weight="bold", expand=True),
            ], vertical_alignment=ft.CrossAxisAlignment.START)

        return ft.Column(
            [
                banner("BIODATA MAHASISWA (DAPAT DIUBAH)"),
                white_card([
                    baris("Nama Lengkap", nama_mhs(nim)),
                    baris("NIM", nim),
                    baris("Fakultas", p["fakultas"]),
                    baris("Program Studi", p["prodi"]),
                    baris("Semester", p["semester"]),
                    baris("Dosen Wali", p["dosen_wali"]),
                    baris("Jenis Kelamin", p["gender"]),
                    baris("Kewarganegaraan", p["kewarganegaraan"]),
                    baris("Tahun Lulus", p["tahun_lulus"]),
                    ft.Divider(),
                    ft.Text("Data Kontak & Pribadi (Bisa Diedit):", weight="bold", color=NAVY),
                    t_hp, t_email, t_agama, t_tgl,
                    ft.ElevatedButton("Simpan Perubahan Biodata", on_click=save_bio,
                                      bgcolor=NAVY, color="white"),
                ], spacing=10, padding=20),
            ],
            expand=True, spacing=10, scroll=ft.ScrollMode.AUTO,
        )

    def menu_keuangan(nim):
        nominal_list = ["Rp 5.500.000", "Rp 6.000.000", "Rp 4.500.000", "Rp 7.000.000"]
        lv = ft.ListView(expand=True, spacing=4)
        for idx, (n, nama) in enumerate(MAHASISWA):
            nominal = nominal_list[idx % len(nominal_list)]
            lv.controls.append(
                ft.Container(
                    bgcolor="#dbeafe" if n == nim else "white", border_radius=6, padding=10,
                    content=ft.Row([
                        ft.Column([
                            ft.Text(nama, size=13, weight="bold"),
                            ft.Text(f"NIM {n} | UKT: {nominal}", size=11, color="#475569"),
                        ], expand=True, spacing=2),
                        ft.Text("LUNAS", color="#15803d", weight="bold", size=12),
                    ]),
                )
            )
        return ft.Column(
            [banner("TAGIHAN & KEUANGAN (UKT) - SEMUA MAHASISWA LUNAS"), lv],
            expand=True, spacing=8)

    def menu_keringanan():
        return ft.Column(
            [banner("PENGAJUAN KERINGANAN UKT"),
             white_card([
                 ft.Text("Status Pengajuan Keringanan UKT: Belum mengajukan.", weight="bold"),
                 ft.ElevatedButton("Ajukan Permohonan Keringanan", bgcolor=NAVY, color="white",
                                   on_click=lambda e: toast("Formulir pengajuan dibuka.")),
             ], spacing=10, padding=20)],
            expand=True, spacing=10)

    def menu_perpus(nim):
        lv = ft.ListView(expand=True, spacing=6)
        lbl = ft.Text("", weight="bold", color=NAVY, size=12)

        def toggle(e):
            judul = e.control.data
            mine = db["pinjam"].setdefault(nim, [])
            if judul in mine:
                mine.remove(judul)
                toast("Buku berhasil dikembalikan.")
            elif len(mine) >= MAKS_PINJAM:
                toast(f"Maksimal peminjaman {MAKS_PINJAM} buku!", True)
                return
            else:
                mine.append(judul)
                toast("Buku berhasil dipinjam.")
            save_db(db)
            render()

        def render():
            mine = db["pinjam"].get(nim, [])
            lbl.value = f"Pinjaman aktif: {len(mine)}/{MAKS_PINJAM} buku"
            lv.controls.clear()
            for buku in BUKU_LIST:
                dipinjam = buku in mine
                lv.controls.append(
                    ft.Container(
                        bgcolor="#ecfdf5" if dipinjam else "white", padding=10, border_radius=6,
                        border=ft.border.all(1, "#a7f3d0" if dipinjam else "#cbd5e1"),
                        content=ft.Row([
                            ft.Icon(ft.Icons.BOOK, color=NAVY),
                            ft.Text(buku, weight="bold", size=12, expand=True),
                            ft.TextButton("Kembalikan" if dipinjam else "Pinjam",
                                          data=buku, on_click=toggle),
                        ]),
                    )
                )
            page.update()

        render()
        return ft.Column(
            [banner(f"KATALOG PERPUSTAKAAN - FISIKA SEMESTER {SEMESTER_AKTIF}"), lbl, lv],
            expand=True, spacing=8)

    def menu_eval():
        return ft.Column(
            [banner("EVALUASI PERKULIAHAN (EDOM)"),
             white_card([ft.Text("Silakan isi kuesioner evaluasi dosen pengampu mata kuliah "
                                 "semester ini.", size=13)], padding=20)],
            expand=True, spacing=10)

    def menu_pedoman():
        def judul(t):
            return ft.Text(t, weight="bold", color=NAVY)

        def butir(t):
            return ft.Text(f"• {t}", size=11)

        return ft.Column(
            [banner("DAFTAR PEDOMAN PROSEDUR RESMI UNIVERSITAS AIRLANGGA"),
             white_card([
                 judul("Direktorat Kemahasiswaan (PP-UNAIR-KMS)"),
                 butir("Layanan Beasiswa Diploma dan Sarjana (PP-UNAIR-KMS-01-01)"),
                 butir("Konsultasi dan Pendampingan / Help Center (PP-UNAIR-KMS-01-02)"),
                 butir("Kegiatan LKMM Tingkat Dasar & Menengah (PP-UNAIR-KMS-02-01)"),
                 ft.Divider(),
                 judul("Direktorat Pendidikan (PP-UNAIR-PBM)"),
                 butir("Pengendalian Registrasi dan Herregistrasi (PP-UNAIR-PBM-01)"),
                 butir("Skripsi / Tugas Akhir (PP-UNAIR-PBM-04)"),
                 butir("Kuliah Kerja Nyata Belajar Bersama Masyarakat (KKN-BBM) "
                       "(PP-UNAIR-PBM-13)"),
                 ft.Divider(),
                 judul("Lembaga Penelitian dan Pengabdian kepada Masyarakat "
                       "(PP-UNAIR-LPPM)"),
                 butir("Penelitian & Pengabdian Kepada Masyarakat (Kerjasama dengan Mitra) "
                       "(PP-UNAIR-LPPM-01)"),
             ], spacing=4, padding=12)],
            expand=True, spacing=10, scroll=ft.ScrollMode.AUTO)

    def get_content(menu, nim):
        if menu == "Home":
            return menu_home(nim)
        if menu == "Biodata":
            return menu_biodata(nim)
        if menu == "Akademik":
            return menu_akademik(nim)
        if menu == "Dosen":
            return menu_dosen()
        if menu == "Keuangan":
            return menu_keuangan(nim)
        if menu == "Keringanan UKT":
            return menu_keringanan()
        if menu == "Perpustakaan":
            return menu_perpus(nim)
        if menu == "Eval":
            return menu_eval()
        return menu_pedoman()

    # ============================================================ HALAMAN UTAMA
    def show_main(nim):
        page.clean()
        state["khs_ok"] = False

        menu_names = ["Home", "Biodata", "Akademik", "Dosen", "Keuangan",
                      "Keringanan UKT", "Perpustakaan", "Eval", "Pedoman"]
        content = ft.Container(expand=True, padding=12, content=get_content("Home", nim))
        tab_buttons = []

        def pilih_menu(e):
            idx = e.control.data
            content.content = get_content(menu_names[idx], nim)
            for i, b in enumerate(tab_buttons):
                b.bgcolor = NAVY if i == idx else "#d9e2ec"
                b.content.color = "white" if i == idx else "#334155"
            page.update()

        for i, nama in enumerate(menu_names):
            tab_buttons.append(
                ft.Container(
                    data=i, on_click=pilih_menu,
                    bgcolor=NAVY if i == 0 else "#d9e2ec",
                    border_radius=ft.border_radius.only(top_left=6, top_right=6),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    content=ft.Text(nama, weight="bold", size=11,
                                    color="white" if i == 0 else "#334155"),
                )
            )

        nama = nama_mhs(nim)
        inisial = "".join(w[0] for w in nama.split()[:2]).upper()
        header = ft.Container(
            bgcolor=NAVY,
            padding=ft.padding.only(left=14, right=6, top=26, bottom=10),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row([
                                ft.Container(
                                    width=36, height=36, border_radius=18,
                                    bgcolor="#d4af3733", alignment=ft.alignment.center,
                                    content=ft.Text("UA", color=GOLD, weight="bold", size=14),
                                ),
                                ft.Column([
                                    ft.Text("CYBER CAMPUS", size=15, weight="bold", color=GOLD),
                                    ft.Text("Universitas Airlangga", size=11, color=GOLD),
                                    ft.Text("Excellence with Morality", size=9, italic=True,
                                            color="white"),
                                ], spacing=0),
                            ], spacing=10),
                            ft.TextButton("Keluar", on_click=lambda e: show_login(),
                                          style=ft.ButtonStyle(color="white")),
                        ],
                    ),
                    ft.Container(
                        bgcolor="#0b3d7a", border_radius=8,
                        padding=ft.padding.symmetric(horizontal=10, vertical=6),
                        content=ft.Row([
                            ft.CircleAvatar(content=ft.Text(inisial, weight="bold", size=11),
                                            radius=14, bgcolor=GOLD, color=NAVY),
                            ft.Text(f"{nama} ({nim})", color="white", size=11, weight="bold",
                                    expand=True, max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                        ], spacing=8),
                    ),
                ],
            ),
        )

        page.add(
            ft.Column(
                [header,
                 ft.Row(tab_buttons, scroll=ft.ScrollMode.AUTO, spacing=2),
                 content],
                expand=True, spacing=0,
            )
        )
        page.update()

    show_login()


ft.app(target=main)