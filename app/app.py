# =[Modules dan Packages]========================

from flask import Flask,render_template,request,jsonify
import pandas as pd
import numpy as np
from joblib import load
import mysql.connector
from mysql.connector import Error

# =[Variabel Global]=============================

app   = Flask(__name__, static_url_path='/static')
model = None

# =[Routing]=====================================

# [Routing untuk Halaman Utama atau Home]	
@app.route("/")
def beranda():
    return render_template('index.html')

# [Routing untuk API]   
@app.route("/deteksi", methods=['GET', 'POST'])
def apiDeteksi():
    if request.method == 'POST':
        try:
            # Extract form data
            nama = request.form['Nama']
            posisi_harapan = request.form['Posisi_Harapan']
            usia = int(request.form['Usia'])
            pendidikan = int(request.form['Pendidikan'])
            lama_pengalaman = int(request.form['Lama_Pengalaman'])
            kesesuaian_posisi_dg_skills = int(request.form['Kesesuaian_Posisi_Skill'])
            kesesuaian_posisi_dg_pengalaman = int(request.form['Kesesuaian_Posisi_Pengalaman'])

            # Perform prediction
            df_test = pd.DataFrame(data={
                "Usia": [usia],
                "Pendidikan": [pendidikan],
                "Lama_Pengalaman": [lama_pengalaman],
                "Kesesuaian_Posisi_Skill": [kesesuaian_posisi_dg_skills],
                "Kesesuaian_Posisi_Pengalaman": [kesesuaian_posisi_dg_pengalaman]
            })
            hasil_prediksi = model.predict(df_test[0:1])[0]

            # Map prediction to a string
            if hasil_prediksi == 1:
                hasil_prediksi_str = 'Recommended Candidate'
            elif hasil_prediksi == 0:
                hasil_prediksi_str = 'Not Recommended Candidate'
            else:
                hasil_prediksi_str = 'Data Tidak Sesuai Dengan Format'

            # Save data to the database
            try:
                connection = mysql.connector.connect(host='localhost',
                                                    database='hasil_prediksi',
                                                    user='root',
                                                    password='')
                if connection.is_connected():
                    cursor = connection.cursor()
                    # Replace 'nama', 'posisi_harapan' with the actual form inputs
                    cursor.execute(f"INSERT INTO klasifikasi (nama, usia, pendidikan, lama_pengalaman, "
                                    f"kesesuaian_posisi_dg_skills, kesesuaian_posisi_dg_pengalaman, "
                                    f"posisi_harapan, hasil_prediksi) "
                                    f"VALUES ('{nama}', {usia}, {pendidikan}, {lama_pengalaman}, "
                                    f"{kesesuaian_posisi_dg_skills}, {kesesuaian_posisi_dg_pengalaman}, "
                                    f"'{posisi_harapan}', '{hasil_prediksi_str}')")
                    connection.commit()
                    print("Data berhasil disimpan ke database.")
            except Error as e:
                print("Error while connecting to MySQL", e)
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection is closed")

            # Return prediction result as JSON
            return jsonify({
                "prediksi": hasil_prediksi_str
            })
        except Exception as e:
            print(f"Error during prediction: {e}")
            return jsonify({
                "error": "Error during prediction"
            })

    # If the request is not POST, render the prediksi.html page
    return render_template('prediksi.html')
            
@app.route("/view_tabel", methods=['GET'])
def view_tabel():
    try:
        connection = mysql.connector.connect(host='localhost',
                                                database='hasil_prediksi',
                                                user='root',
                                                password='')
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM klasifikasi")
            data_tabel = cursor.fetchall()
            return render_template('view_tabel.html', data_tabel=data_tabel)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            
            
# =[Main]========================================

if __name__ == '__main__':
	
	# Load model yang telah ditraining
	model = load('model_klasifikasi_dctc45.model')

	# Run Flask di localhost 
	app.run(host="localhost", port=5000, debug=True)