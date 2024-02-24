from difflib import get_close_matches as yakin_sonuc
from tkinter import filedialog
import tkinter as tk
import json

def veritabanini_yukle(dosya_yolu):
    with open(dosya_yolu, "r") as dosya:
        return json.load(dosya)

def veritabanina_yaz(veriler, dosya_yolu):
    with open(dosya_yolu, "w") as dosya:
        json.dump(veriler, dosya, indent=2)

def yakin_sonuc_bul(soru, sorular):
    eslesen = yakin_sonuc(soru, sorular, n=1, cutoff=0.6)
    return eslesen[0] if eslesen else None

def cevabini_bul(soru, veritabanimiz):
    for soru_cevaplar in veritabanimiz["sorular"]:
        if soru_cevaplar["soru"] == soru:
            return soru_cevaplar["cevap"]
    return None

def chat_bot():
    print("Chat Bot: Merhaba! Benimle konuşmaya başlayabilirsiniz. 'çik' yazarak konuşmayi sonlandirabilirsiniz.")
    
    # Arayüz Oluşturma
    arayuz = tk.Tk()
    arayuz.title("Chat Bot Arayüzü")
    arayuz.geometry("400x200")
    
    dosya_yolu_label = tk.Label(arayuz, text="Veritabanı Dosyası:")
    dosya_yolu_label.grid(row=0, column=0, padx=10, pady=10)
    
    def dosya_sec():
        dosya_yolu = filedialog.askopenfilename(title="Veritabanı Dosyasını Seç", filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
        if dosya_yolu:
            dosya_yolu_entry.delete(0, tk.END)
            dosya_yolu_entry.insert(0, dosya_yolu)
    
    dosya_sec_button = tk.Button(arayuz, text="Dosya Seç", command=dosya_sec)
    dosya_sec_button.grid(row=0, column=1, padx=10, pady=10)
    
    dosya_yolu_entry = tk.Entry(arayuz, width=50)
    dosya_yolu_entry.grid(row=0, column=2, padx=10, pady=10)
    
    def baslat():
        dosya_yolu = dosya_yolu_entry.get()
        if not dosya_yolu:
            tk.messagebox.showwarning("Uyarı", "Lütfen bir veritabanı dosyası seçin!")
            return
        
        veritabani = veritabanini_yukle(dosya_yolu)
        while True:
            soru = input("Siz: ")
            
            if soru.lower() == "çik":
                print("Chat Bot: Hoşça kal! İyi günler.")
                break
    
            gelen_sonuc = yakin_sonuc_bul(soru, [soru_cevaplar["soru"] for soru_cevaplar in veritabani["sorular"]])
            
            if gelen_sonuc:
                cevap = cevabini_bul(gelen_sonuc, veritabani)
                if cevap:
                    print("Chat Bot:", cevap)
                else:
                    print("Chat Bot: Ne demek istediğinizi anlayamadim.")
            else:
                print("Chat Bot: Üzgünüm, bir sonuç bulunamadi.")
                yeni_cevap = input("Chat Bot: Ancak, bu sorunun cevabini benimle paylaşabilir misiniz? Cevap: ")
                
                if yeni_cevap:
                    yeni_soru_cevap = {"soru": soru, "cevap": yeni_cevap}
                    veritabani["sorular"].append(yeni_soru_cevap)
                    veritabanina_yaz(veritabani, dosya_yolu)
                    print("Chat Bot: Yeni soru-cevap eklendi. Teşekkür ederim!")
                else:
                    print("Chat Bot: Anladim, başka bir sorunuz var mi?")
    
    baslat_button = tk.Button(arayuz, text="Başlat", command=baslat)
    baslat_button.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
    
    arayuz.mainloop()

if __name__ == '__main__':
    chat_bot()
