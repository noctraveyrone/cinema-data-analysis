
import pandas as pd
import plotly.express as px
import webbrowser
import os
import plotly.graph_objects as go
# CSV dosyasını oku
df_url ="veri_dosyası5.csv"
df = pd.read_csv(df_url)
#*******************************************************************************************************************************************



# Yıl bazında izleyici sayısını toplama
yil_bazinda_izleyici = df.groupby('Vizyona Giriş Yılı')['Izleyici Sayısı'].sum().reset_index()

# Sinema salonları ve koltuk sayıları verisi
data_sinema = {
    "Yıl": [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Sinema Salonları Sayısı": [1514, 1647, 1834, 1917, 1998, 2102, 2170, 2356, 2483, 2692, 2858, 2826, 2698, 2398, 2366, 2618, 2863]
}
df_sinema = pd.DataFrame(data_sinema)

# Yıl ve sinema verilerini birleştirme
merged_df = pd.merge(df_sinema, yil_bazinda_izleyici, left_on='Yıl', right_on='Vizyona Giriş Yılı')
merged_df['Ortalama Izleyici Sayısı'] = merged_df['Izleyici Sayısı'] / merged_df['Sinema Salonları Sayısı']

# Korelasyon hesaplama
korelasyon = merged_df['Sinema Salonları Sayısı'].corr(merged_df['Ortalama Izleyici Sayısı'])

# Korelasyonu yazdırma
print(f"Sinema Salonları Sayısı ile Ortalama İzleyici Sayısı arasındaki korelasyon: {korelasyon:.2f}")

# Korelasyonu grafikle gösterme
fig_korelasyon = px.scatter(merged_df, x='Sinema Salonları Sayısı', y='Ortalama Izleyici Sayısı',
                            trendline='ols', title='Sinema Salonları Sayısı ile Ortalama İzleyici Sayısı Arasındaki Korelasyon',
                            labels={'Sinema Salonları Sayısı': 'Sinema Salonları Sayısı', 'Ortalama Izleyici Sayısı': 'Ortalama İzleyici Sayısı'})
fig_korelasyon.update_layout(width=800, height=600)
fig_korelasyon_path = os.path.abspath("korelasyon_grafik.html")
fig_korelasyon.write_html(fig_korelasyon_path)

# Yıl bazında film sayısını toplama
yil_bazinda_film_sayisi = df.groupby('Vizyona Giriş Yılı')['Film Adı'].count().reset_index()
yil_bazinda_film_sayisi.columns = ['Vizyona Giriş Yılı', 'Film Sayısı']
# Yıl bazında izleyici başına düşen ortalama film izleyici sayısını hesaplama
yil_bazinda_izleyici['Ortalama Izleyici Sayısı'] = yil_bazinda_izleyici['Izleyici Sayısı'] / yil_bazinda_film_sayisi['Film Sayısı']

#1. grafik Yıl bazında ortalama izleyici sayısındaki değişim
fig1 = px.line(yil_bazinda_izleyici, x='Vizyona Giriş Yılı', y='Ortalama Izleyici Sayısı',
            title='Yıl Bazında Ortalama İzleyici Sayısındaki Değişim',
            labels={'Vizyona Giriş Yılı': 'Vizyona Giriş Yılı', 'Ortalama Izleyici Sayısı': 'Ortalama İzleyici Sayısı (Film Başına)'})
fig1.update_traces(hoverinfo='x+y+text')
fig1_path = os.path.abspath("yil_bazinda_grafik.html")
fig1.write_html(fig1_path)

# Sinema salonları ve koltuk sayıları verisi
data_sinema = {
    "Yıl": [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Sinema Salonları Sayısı": [1514, 1647, 1834, 1917, 1998, 2102, 2170, 2356, 2483, 2692, 2858, 2826, 2698, 2398, 2366, 2618, 2863]
}
df_sinema = pd.DataFrame(data_sinema)

# Figürü ve iki ekseni oluşturma
fig = go.Figure()

# Sinema salonları sayısı verisi için mavi çizgi ekleyelim
fig.add_trace(go.Scatter(x=df_sinema['Yıl'], y=df_sinema['Sinema Salonları Sayısı'],
                         mode='lines+markers',
                         name='Sinema Salonları Sayısı',
                         line=dict(color='blue'),
                         line_shape='spline'))


# Ekseni başlıklarını ve layout ayarlarını yapalım
fig.update_layout(
    title='Yıl Bazında Sinema Salonların sayısındaki değişim',
    xaxis=dict(title='Yıl'),
    yaxis=dict(title='Sinema Salonları Sayısı', titlefont=dict(color='blue'), tickfont=dict(color='blue')),
   
    legend=dict(x=1.1, y=1.1),
    width=1200,
    height=600
)

# Grafiği HTML olarak kaydedelim
fig2_path = os.path.abspath("sinema_salonlari_koltuklari_grafik.html")
fig.write_html(fig2_path)

# Yıl bazında film sayısını yazdırma ve HTML dosyasına ekleme
film_sayisi_html = '<h3>Yıl Bazında Film Sayısı Tablosu</h3><table><tr><th>Yıl</th><th>Film Sayısı</th></tr>'
for index, row in yil_bazinda_film_sayisi.iterrows():
    film_sayisi_html += f'<tr><td>{row["Vizyona Giriş Yılı"]}</td><td>{row["Film Sayısı"]}</td></tr>'
film_sayisi_html += '</table>'
# Yıl bazında ortalama izleyici sayısını yazdırma ve HTML dosyasına ekleme
ortalama_html = '<h3>Yıl Bazında Ortalama İzleyici Sayısı (Film Başına)</h3><ul>'
for index, row in yil_bazinda_izleyici.iterrows():
    ortalama_html += f'<li>{row["Vizyona Giriş Yılı"]} yılı: {row["Ortalama Izleyici Sayısı"]:.2f} izleyici/film</li>'
ortalama_html += '</ul>'
# Ortalama izleyici sayısını gösteren pasta grafik oluşturma
fig4 = px.pie(yil_bazinda_izleyici, names='Vizyona Giriş Yılı', values='Ortalama Izleyici Sayısı',
              title='Yıl Bazında Ortalama İzleyici Sayısı (Film Başına)',
              labels={'Vizyona Giriş Yılı': 'Vizyona Giriş Yılı', 'Ortalama Izleyici Sayısı': 'Ortalama İzleyici Sayısı'})
fig4.update_traces(textinfo='percent+label')
fig4.update_layout(width=750, height=550) # Grafiği büyütme
fig4_path = os.path.abspath("ortalama_izleyici_sayisi_grafik.html")
fig4.write_html(fig4_path)
# Yıl bazında film sayısını gösteren pasta grafik oluşturma
fig5 = px.pie(yil_bazinda_film_sayisi, names='Vizyona Giriş Yılı', values='Film Sayısı',
              title='Yıl Bazında Film Sayısı',
              labels={'Vizyona Giriş Yılı': 'Vizyona Giriş Yılı', 'Film Sayısı': 'Film Sayısı'})
fig5.update_traces(textinfo='percent+label')
fig5.update_layout(width=600, height=550)  # Grafiği küçültme
fig5_path = os.path.abspath("film_sayisi_yıl_grafik.html")
fig5.write_html(fig5_path)

# HTML dosyasını oluşturma ve güncelleme
with open('combined_yıl_grafik.html', 'w', encoding='utf-8') as f:
    f.write('<html><body>')
    f.write('<h2>Yıllara Göre İzleyici Sayısındaki Değişim</h2>')
    f.write('<iframe src="' + fig1_path + '" width="100%" height="600"></iframe>')
    
    f.write('<h2>Yıllara Göre Sinema Salonları Sayısındaki Değişim</h2>')
    f.write('<iframe src="' + fig2_path + '" width="100%" height="600"></iframe>')

    f.write('<h2>Sinema Salonları Sayısı ile Ortalama İzleyici Sayısı Arasındaki Korelasyon</h2>')
    f.write('<iframe src="' + fig_korelasyon_path + '" width="100%" height="600"></iframe>')

    f.write('<h2>Yıl Bazında Ortalama İzleyici Sayısı ve Film Sayısı</h2>')
    f.write('<iframe src="' + fig4_path + '" width="48%" height="400"></iframe>')
    f.write('<iframe src="' + fig5_path + '" width="48%" height="400"></iframe>')
    f.write('</body></html>')

webbrowser.open('file://' + os.path.abspath("combined_yıl_grafik.html"))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Mevsimlere göre izleyici sayısını toplama
mevsim_bazinda_izleyici = df.groupby('Yayınlanma Mevsimi')['Izleyici Sayısı'].sum().reset_index()
mevsim_sirasi = ['İlkbahar', 'Yaz', 'Sonbahar', 'Kış']
mevsim_bazinda_izleyici['Yayınlanma Mevsimi'] = pd.Categorical(mevsim_bazinda_izleyici['Yayınlanma Mevsimi'], categories=mevsim_sirasi, ordered=True)
mevsim_bazinda_izleyici = mevsim_bazinda_izleyici.sort_values('Yayınlanma Mevsimi')
# Mevsim bazında film sayısını toplama
mevsim_bazinda_film_sayisi = df.groupby('Yayınlanma Mevsimi')['Film Adı'].count().reset_index()
mevsim_bazinda_film_sayisi.columns = ['Yayınlanma Mevsimi', 'Film Sayısı']
# Mevsim bazında izleyici başına düşen ortalama film izleyici sayısını hesaplama
mevsim_bazinda_izleyici['Ortalama Izleyici Sayısı'] = mevsim_bazinda_izleyici['Izleyici Sayısı'] / mevsim_bazinda_film_sayisi['Film Sayısı']
# Kontrol adımları
print(mevsim_bazinda_izleyici)
print(mevsim_bazinda_film_sayisi)
print(mevsim_bazinda_izleyici[['Yayınlanma Mevsimi', 'Ortalama Izleyici Sayısı']])

# 2. Grafik: Mevsimlere Göre İzleyici Sayısındaki Değişim
fig2 = px.bar(mevsim_bazinda_izleyici, x='Yayınlanma Mevsimi', y='Ortalama Izleyici Sayısı',
              title='Mevsimlere Göre Ortalama İzleyici Sayısındaki Değişim',
              labels={'Yayınlanma Mevsimi': 'Yayınlanma Mevsimi', 'Izleyici Sayısı': 'Ortalama İzleyici Sayısı'},
              text='Ortalama Izleyici Sayısı')

fig2.update_traces(hoverinfo='none')
fig2.update_layout(width=1400, height=600) # Grafiği küçültme
fig2_path = os.path.abspath("mevsim_bazinda_grafik.html")
fig2.write_html(fig2_path)

# Mevsim bazında film sayısını yazdırma ve HTML dosyasına ekleme
film_sayisi_mevsim_html = '<h3>Mevsim Bazında Film Sayısı Tablosu</h3><table><tr><th>Mevsim</th><th>Film Sayısı</th></tr>'
for index, row in mevsim_bazinda_film_sayisi.iterrows():
    film_sayisi_mevsim_html += f'<tr><td>{row["Yayınlanma Mevsimi"]}</td><td>{row["Film Sayısı"]}</td></tr>'
film_sayisi_mevsim_html += '</table>'

# Ortalama izleyici sayısını gösteren pasta grafik oluşturma
fig5 = px.pie(mevsim_bazinda_izleyici, names='Yayınlanma Mevsimi', values='Ortalama Izleyici Sayısı',
              title='Mevsim Bazında Ortalama İzleyici Sayısı (Film Başına)',
              labels={'Yayınlanma Mevsimi': 'Yayınlanma Mevsimi', 'Ortalama Izleyici Sayısı': 'Ortalama İzleyici Sayısı'})
fig5.update_traces(textinfo='percent+label')
fig5.update_layout(width=700, height=500)  # Grafiği küçültme
fig5_path = os.path.abspath("ortalama_izleyici_sayisi_mevsim_grafik.html")
fig5.write_html(fig5_path)
# Ortalama film sayısını gösteren pasta grafik oluşturma

fig6 = px.pie(mevsim_bazinda_film_sayisi, names='Yayınlanma Mevsimi', values='Film Sayısı',
              title='Mevsim Bazında Film Sayısı',
              labels={'Yayınlanma Mevsimi': 'Yayınlanma Mevsimi', 'Film Sayısı': 'Film Sayısı'})
fig6.update_traces(textinfo='percent+label')
fig6.update_layout(width=600, height=500)  # Grafiği küçültme
fig6_path = os.path.abspath("film_sayisi_mevsim_grafik.html")
fig6.write_html(fig6_path)

# HTML dosyasını oluşturma ve güncelleme
with open('combined_mevsim_grafik.html', 'w', encoding='utf-8') as f:
    f.write('<html><body>')
    # Sütun grafiği ekleme (Sadece bir kez)
    f.write('<h2>Mevsimlere Göre İzleyici Sayısındaki Değişim</h2>')
    f.write('<iframe src="' + fig2_path + '" width="100%" height="600"></iframe>')
    
    # Pasta grafiklerini alt alta ekleme
    f.write('<h2>Mevsim Bazında Ortalama İzleyici Sayısı ve Film Sayısı</h2>')
    f.write('<iframe src="' + fig5_path + '" width="48%" height="400"></iframe>')
    f.write('<iframe src="' + fig6_path + '" width="48%" height="400"></iframe>')
    f.write('</body></html>')

webbrowser.open('file://' + os.path.abspath("combined_mevsim_grafik.html"))

# Açıklamalar:
# 1. `fig2.write_html(fig2_path)`: Bu satır mevsim bazında izleyici sayısını gösteren grafiği oluşturur ve HTML dosyasına yazar.
# 2. `fig5.write_html(fig5_path)` ve `fig6.write_html(fig6_path)`: Bu satırlar mevsim bazında izleyici sayısı ve film sayısını gösteren pasta grafiklerini oluşturur ve HTML dosyasına yazar.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Film türüne göre izleyici sayısını toplama
tur_bazinda_izleyici = df.groupby('Film Türü')['Izleyici Sayısı'].sum().reset_index()
tur_bazinda_izleyici = tur_bazinda_izleyici.sort_values(by='Izleyici Sayısı', ascending=False)

# İlk 16 tür ve "Diğerleri" olarak kodlama
top_16_tur = tur_bazinda_izleyici.head(16)
other_tur = pd.DataFrame(data={
    'Film Türü': ['Diğerleri'],
    'Izleyici Sayısı': [tur_bazinda_izleyici.iloc[16:]['Izleyici Sayısı'].sum()]
})
top_16_tur = pd.concat([top_16_tur, other_tur], ignore_index=True)

# Film türüne göre film sayısını toplama
tur_bazında_film_sayisi = df.groupby('Film Türü')['Film Adı'].count().reset_index()
tur_bazında_film_sayisi.columns = ['Film Türü', 'Film Sayısı']
tur_bazında_film_sayisi['Film Türü'] = tur_bazında_film_sayisi['Film Türü'].apply(lambda x: x if x in top_16_tur['Film Türü'].values else 'Diğerleri')
tur_bazında_film_sayisi = tur_bazında_film_sayisi.groupby('Film Türü').sum().reset_index()

# Tür bazında izleyici başına düşen ortalama film izleyici sayısını hesaplama
top_16_tur['Film Sayısı'] = top_16_tur['Film Türü'].map(tur_bazında_film_sayisi.set_index('Film Türü')['Film Sayısı'])
top_16_tur['Ortalama Izleyici Sayısı'] = top_16_tur['Izleyici Sayısı'] / top_16_tur['Film Sayısı']

# 3. Grafik: Film Türüne Göre İzleyici Sayısındaki Değişim
fig16 = px.bar(top_16_tur, x='Film Türü', y='Ortalama Izleyici Sayısı',
               title='Film Türüne Göre Ortalama İzleyici Sayısı',
               labels={'Film Türü': 'Film Türü', 'Izleyici Sayısı': 'Ortalama İzleyici Sayısı'},
               text='Ortalama Izleyici Sayısı')

fig16.update_traces(hoverinfo='x+y+text')
fig16.update_layout(width=1400, height=700)  # Grafiği küçültme
fig16_path = os.path.abspath("tur_bazinda_izleyici_grafik.html")
fig16.write_html(fig16_path)


# Grafik: Film Türüne Göre Film Sayısı Pasta Grafiği
fig17 = px.pie(tur_bazında_film_sayisi, names='Film Türü', values='Film Sayısı',
               title='Film Türüne Göre Film Sayısı',
               labels={'Film Türü': 'Film Türü', 'Film Sayısı': 'Film Sayısı'})
fig17.update_traces(textinfo='percent+label')
fig17.update_layout(width=900, height=700)  # Grafiği büyütme
fig17_path = os.path.abspath("tur_bazında_film_sayisi_grafik.html")
fig17.write_html(fig17_path)

# Film Türüne Göre Ortalama İzleyici Sayısı Pasta Grafiği
fig18 = px.pie(top_16_tur, names='Film Türü', values='Ortalama Izleyici Sayısı',
               title='Film Türüne Göre Ortalama İzleyici Sayısı (Film Başına)',
               labels={'Film Türü': 'Film Türü', 'Ortalama Izleyici Sayısı': 'Ortalama İzleyici Sayısı'})
fig18.update_traces(textinfo='percent+label')
fig18.update_layout(width=900, height=700)  # Grafiği büyütme
fig18_path = os.path.abspath("tur_bazında_ortalama_izleyici_sayisi_grafik.html")
fig18.write_html(fig18_path)

# HTML dosyasını oluşturma ve güncelleme
with open('combined_tur_grafik.html', 'w', encoding='utf-8') as f:
    f.write('<html><body>')
    # Film türüne göre izleyici sayısı grafiği (Sütun grafiği)
    f.write('<h2>Film Türüne Göre İzleyici Sayısı</h2>')
    f.write('<iframe src="' + fig16_path + '" width="100%" height="800"></iframe>')
    # Film türüne göre film sayısı grafiği (Pasta grafiği)
    f.write('<h2>Film Türüne Göre Film Sayısı</h2>')
    f.write('<iframe src="' + fig17_path + '" width="100%" height="700"></iframe>')
    # Film türüne göre ortalama izleyici sayısı grafiği (Pasta grafiği)
    f.write('<h2>Film Türüne Göre Ortalama İzleyici Sayısı</h2>')
    f.write('<iframe src="' + fig18_path + '" width="100%" height="700"></iframe>')
    f.write('</body></html>')

webbrowser.open('file://' + os.path.abspath("combined_tur_grafik.html"))
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Yerli ve yabancı filmleri izleyici sayısına göre toplama
yerli_yabanci_bazinda_izleyici = df.groupby('Yerli/Yabancı')['Izleyici Sayısı'].sum().reset_index()
yerli_yabanci_bazinda_film_sayisi = df.groupby('Yerli/Yabancı')['Film Adı'].count().reset_index()
yerli_yabanci_bazinda_film_sayisi.columns = ['Yerli/Yabancı', 'Film Sayısı']

# Ortalama izleyici sayısını hesaplama
yerli_yabanci_bazinda_izleyici['Ortalama Izleyici Sayısı'] = yerli_yabanci_bazinda_izleyici['Izleyici Sayısı'] / yerli_yabanci_bazinda_film_sayisi['Film Sayısı']

# Yerli ve yabancı filmleri içeren dataframe oluşturma
yerli_yabanci_bazinda = yerli_yabanci_bazinda_izleyici.merge(yerli_yabanci_bazinda_film_sayisi, on='Yerli/Yabancı')

# Yıl bazında yerli ve yabancı izleyici sayısını toplama
yil_yerli_yabanci_izleyici = df.groupby(['Vizyona Giriş Yılı', 'Yerli/Yabancı'])['Izleyici Sayısı'].sum().reset_index()


# Yıl ve yerli/yabancı türlerine göre sütun grafiği oluşturma
fig = px.bar(yil_yerli_yabanci_izleyici, x='Vizyona Giriş Yılı', y='Izleyici Sayısı', color='Yerli/Yabancı', barmode='group',
             title='Yıllara Göre Yerli ve Yabancı Film İzleyici Sayıları (Toplam)',
             labels={'Vizyona Giriş Yılı': 'Yıl', 'Izleyici Sayısı': 'İzleyici Sayısı', 'Yerli/Yabancı': 'Film Türü'},
             width=1200, height=600)

# Grafiği HTML olarak kaydedelim
fig_path = os.path.abspath("yillara_gore_yerli_yabanci_izleyici_grafik.html")
fig.write_html(fig_path)

# 4.grafik Sütun grafiği oluşturma
fig_yerliyabanci_bar = px.bar(yerli_yabanci_bazinda, x='Yerli/Yabancı', y='Ortalama Izleyici Sayısı',
                              title='Yerli ve Yabancı Filmlerin Ortalama İzleyici Sayıları',
                              labels={'Yerli/Yabancı': 'Film Türü', 'Ortalama Izleyici Sayısı': 'Ortalama İzleyici Sayısı'},
                              text='Ortalama Izleyici Sayısı',
                              width=800, height=600)

# Sütun genişliklerini ayarlama
fig_yerliyabanci_bar.update_layout(bargap=0.5)

fig_yerliyabanci_bar_path = os.path.abspath("yerli_yabanci_bar_grafik.html")
fig_yerliyabanci_bar.write_html(fig_yerliyabanci_bar_path)

# Pasta grafiği oluşturma (Ortalama izleyici sayısı)
fig_yerliyabanci_pie = px.pie(yerli_yabanci_bazinda, names='Yerli/Yabancı', values='Ortalama Izleyici Sayısı',
                              title='Yerli ve Yabancı Filmlerin Ortalama İzleyici Oranları',
                              labels={'Yerli/Yabancı': 'Film Türü', 'Ortalama Izleyici Sayısı': 'Ortalama İzleyici Sayısı'})

fig_yerliyabanci_pie.update_traces(textinfo='percent+label')
fig_yerliyabanci_pie.update_layout(width=800, height=600)
fig_yerliyabanci_pie_path = os.path.abspath("yerli_yabanci_pie_grafik.html")
fig_yerliyabanci_pie.write_html(fig_yerliyabanci_pie_path)

# Pasta grafiği oluşturma (Film sayısı)
fig_yerliyabanci_count_pie = px.pie(yerli_yabanci_bazinda_film_sayisi, names='Yerli/Yabancı', values='Film Sayısı',
                                    title='Yerli ve Yabancı Filmlerin Sayısı',
                                    labels={'Yerli/Yabancı': 'Film Türü', 'Film Sayısı': 'Film Sayısı'})

fig_yerliyabanci_count_pie.update_traces(textinfo='percent+label')
fig_yerliyabanci_count_pie.update_layout(width=800, height=600)
fig_yerliyabanci_count_pie_path = os.path.abspath("yerli_yabanci_count_pie_grafik.html")
fig_yerliyabanci_count_pie.write_html(fig_yerliyabanci_count_pie_path)

# HTML dosyasını oluşturma ve güncelleme
html_file_path = "combined_grafikler.html"
with open('combined_yerli_yabanci_grafik.html', 'w', encoding='utf-8') as f:
    f.write('<html><body>')
    f.write('<h2>Yıllara Göre Yerli ve Yabancı Film İzleyici Sayıları (Toplam)</h2>')
    f.write('<iframe src="' + fig_path + '" width="100%" height="600"></iframe>')
    
    # Sütun grafiği ekleme
    f.write('<h2>Yerli ve Yabancı Filmlerin Ortalama İzleyici Sayıları</h2>')
    f.write('<iframe src="' + fig_yerliyabanci_bar_path + '" width="100%" height="600"></iframe>')
    # Ortalama izleyici sayısı pasta grafiği ekleme
    f.write('<h2>Yerli ve Yabancı Filmlerin Ortalama İzleyici Oranları</h2>')
    f.write('<iframe src="' + fig_yerliyabanci_pie_path + '" width="100%" height="600"></iframe>')
    # Film sayısı pasta grafiği ekleme
    f.write('<h2>Yerli ve Yabancı Filmlerin Sayısı</h2>')
    f.write('<iframe src="' + fig_yerliyabanci_count_pie_path + '" width="100%" height="600"></iframe>')
   
    f.write('</body></html>')
webbrowser.open('file://' + os.path.abspath("combined_yerli_yabanci_grafik.html"))
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 'IMDb Puanı' sütununu sayısal tipe dönüştürün
df['IMDb Puanı'] = pd.to_numeric(df['IMDb Puanı'], errors='coerce')


#En çok izlenen ilk 20 filmi IMDb puanına ve izleyici sayısına göre sıralama
top_20_films = df.sort_values(by=['IMDb Puanı', 'Izleyici Sayısı'], ascending=[False, False]).nlargest(20, 'IMDb Puanı')[['Film Adı', 'IMDb Puanı', 'Izleyici Sayısı']]

# 4.grafik IMDb Puanına Göre En Çok İzlenen İlk 20 Film
left_column = top_20_films.iloc[:10].reset_index(drop=True)
right_column = top_20_films.iloc[10:].reset_index(drop=True)

# Sonucu yazdırma
output = []
for i in range(10):
    left_film = f"<span class='tooltip'><b>{i+1}. {left_column.at[i, 'Film Adı']}</b><span class='tooltiptext'>IMDb: {left_column.at[i, 'IMDb Puanı']}<br>İzleyici: {left_column.at[i, 'Izleyici Sayısı']}</span></span>"
    right_film = ""
    if i < len(right_column):
        right_film = f"<span class='tooltip'><b>{i+11}. {right_column.at[i, 'Film Adı']}</b><span class='tooltiptext'>IMDb: {right_column.at[i, 'IMDb Puanı']}<br>İzleyici: {right_column.at[i, 'Izleyici Sayısı']}</span></span>"
    output.append(f"<tr><td style='padding-right: 40px;'>{left_film}</td><td>{right_film}</td></tr>")

# Her yılın en çok izlenen filmini bulma
most_watched_per_year = df.loc[df.groupby('Vizyona Giriş Yılı')['Izleyici Sayısı'].idxmax(), ['Vizyona Giriş Yılı', 'Film Adı', 'Yönetmen', 'IMDb Puanı', 'Ülke', 'Izleyici Sayısı']].reset_index(drop=True)
# HTML dosyasını oluşturma
with open('imdb_listesi.html', 'w', encoding='utf-8') as f:
    f.write('<html><head><style>')
    f.write('body {font-family: Arial, sans-serif; background-color: #e9ecef; margin: 0; padding: 20px;}')
    
    # Tablo stili
    f.write('table {border-collapse: collapse; width: 100%; margin-bottom: 20px; background-color: #ffffff; border-radius: 8px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);}')
    f.write('td {padding: 6px 8px; font-size: 13px; color: #333; vertical-align: top;}')  # Yazı boyutu küçültüldü ve sağ-sol mesafe azaltıldı
    f.write('tr:nth-child(even) {background-color: #f8f9fa;}')  # Alternatif satır rengi
    f.write('h3 {color: #333; font-size: 1.3em; margin-top: 20px; text-align: center; border-bottom: 2px solid #adb5bd; padding-bottom: 10px;}')
    
    # Tooltip stili
    f.write('.tooltip {position: relative; display: inline-block; cursor: pointer;}')
    f.write('.tooltip .tooltiptext {visibility: hidden; width: 220px; background-color: #333; color: #fff; text-align: center; border-radius: 5px; padding: 5px 0; position: absolute; z-index: 1; bottom: 125%; left: 50%; margin-left: -110px; opacity: 0; transition: opacity 0.3s;}')
    f.write('.tooltip:hover .tooltiptext {visibility: visible; opacity: 1;}')
    
    # Alt kısım için stil
    f.write('.two-column {display: flex; justify-content: space-between; margin-top: 10px; gap: 20px;}')
    f.write('.column {width: 48%; background-color: #ffffff; padding: 8px; border-radius: 8px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); font-size: 12px;}')  # Font boyutu daha küçük, padding azaltıldı
    f.write('.column p {margin: 6px 0; color: #555; line-height: 1.4;}')
    f.write('.column hr {border: 0; height: 1px; background-color: #dee2e6; margin: 10px 0;}')
    
    # Ortalanmış büyük başlık stili
    f.write('.main-title {text-align: center; font-size: 1.5em; color: #495057; margin-top: 30px; margin-bottom: 20px; font-weight: bold;}')
    f.write('.section-title {text-align: center; font-size: 1.3em; color: #495057; margin-top: 20px; font-weight: bold; border-bottom: 2px solid #adb5bd; padding-bottom: 10px;}')
    
    f.write('</style></head><body>')

    # Üst başlık
    f.write('<div class="section-title">Yıllar Arası En İyi 20 Film</div>')

    # IMDb top 20 filmler tablosu
    f.write('<table>')
    f.write('\n'.join(output))
    f.write('</table>')

    # Alt başlık
    f.write('<div class="main-title">Yıllara Göre En Çok İzlenen Filmler</div>')

    # Yıllık en çok izlenen filmler bölümü (iki sütun)
    f.write('<div class="two-column">')
    
    # Sol sütun
    f.write('<div class="column">')
    for i, (_, row) in enumerate(most_watched_per_year.iterrows()):
        if i % 2 == 0:
            f.write(f"<p><b>{row['Vizyona Giriş Yılı']}:</b> {row['Film Adı']}<br>")
            f.write(f"<b>Yönetmen:</b> {row['Yönetmen']}<br>")
            f.write(f"<b>IMDb Puanı:</b> {row['IMDb Puanı']}<br>")
            f.write(f"<b>Ülke:</b> {row['Ülke']}<br>")
            f.write(f"<b>İzleyici Sayısı:</b> {row['Izleyici Sayısı']:,}</p><hr>")
    f.write('</div>')

    # Sağ sütun
    f.write('<div class="column">')
    for i, (_, row) in enumerate(most_watched_per_year.iterrows()):
        if i % 2 != 0:
            f.write(f"<p><b>{row['Vizyona Giriş Yılı']}:</b> {row['Film Adı']}<br>")
            f.write(f"<b>Yönetmen:</b> {row['Yönetmen']}<br>")
            f.write(f"<b>IMDb Puanı:</b> {row['IMDb Puanı']}<br>")
            f.write(f"<b>Ülke:</b> {row['Ülke']}<br>")
            f.write(f"<b>İzleyici Sayısı:</b> {row['Izleyici Sayısı']:,}</p><hr>")
    f.write('</div>')

    f.write('</div></body></html>')


imdb_listesi_path = os.path.abspath('imdb_listesi.html')
webbrowser.open('file://' + imdb_listesi_path)


