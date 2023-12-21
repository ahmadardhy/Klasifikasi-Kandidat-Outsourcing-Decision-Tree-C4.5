$(document).ready(function(){
  // [Prediksi Model]---------------------------

  // Fungsi untuk memanggil API ketika tombol prediksi ditekan
  $("#prediksi_submit").click(function(e) {
      e.preventDefault();

      // Set data pengukuran bunga iris dari input pengguna
      var nama = $("#input_Nama").val();
      var posisi_harapan = $("#input_Posisi_Harapan").val();
      var usia = $("#range_Usia").val(); 
      var pendidikan  = $("#range_Pendidikan").val(); 
      var lama_pengalaman = $("#range_Lama_Pengalaman").val(); 
      var kesesuaian_posisi_dg_skills = $("#range_Kesesuaian_Posisi_Skill").val(); 
      var kesesuaian_posisi_dg_pengalaman = $("#range_Kesesuaian_Posisi_Pengalaman").val(); 

      // Panggil API dengan timeout 1 detik (1000 ms)
      setTimeout(function() {
          try {
              $.ajax({
                  url  : "/deteksi",
                  type : "POST",
                  data : {
                      "Nama": nama,
                      "Posisi_Harapan": posisi_harapan,
                      "Usia" : usia,
                      "Pendidikan"  : pendidikan,
                      "Lama_Pengalaman" : lama_pengalaman,
                      "Kesesuaian_Posisi_Skill"  : kesesuaian_posisi_dg_skills,
                      "Kesesuaian_Posisi_Pengalaman" : kesesuaian_posisi_dg_pengalaman
                  },
                  success:function(res){
                      // Ambil hasil prediksi spesies dari API
                      var res_data_prediksi = res['prediksi'];
                      
                      // Tampilkan hasil prediksi ke halaman web
                      generate_prediksi(res_data_prediksi);
                  }
              });
          }
          catch(e) {
              // Jika gagal memanggil API, tampilkan error di console
              console.log("Gagal !");
              console.log(e);
          } 
      }, 1000);
  })

  // Fungsi untuk menampilkan hasil prediksi di halaman HTML
  function generate_prediksi(res_data_prediksi) {
      console.log("Result Data Prediksi:", res_data_prediksi);
      
      $("#hasil_prediksi").empty();

      // Tampilkan hasil prediksi ke elemen dengan id "hasil_prediksi"
      $("#hasil_prediksi").html("Hasil Prediksi: " + res_data_prediksi);

      // Tambahkan gambar berdasarkan hasil prediksi
      if (res_data_prediksi == 'Recommended Candidate') {
          // Gambar centang hijau
          console.log("Appending Centang Hijau");
          $("#hasil_prediksi").append("<img src='/static/images/centang_hijau.png' alt='Centang Hijau' width='50'>");
      } else if (res_data_prediksi == 'Not Recommended Candidate') {
          // Gambar silang merah
          console.log("Appending Silang Merah");
          $("#hasil_prediksi").append("<img src='/static/images/silang_merah.png' alt='Silang Merah' width='50'>");
      } else {
          console.log("No image appended. Prediction: ", res_data_prediksi);
      }
  }
});
