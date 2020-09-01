var app = new Vue({
  el: '#app',
  data: {
    tasks: null,
    axiosConfig: {
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
        "Access-Control-Allow-Origin": "*",
      }
    },
    form: {
      nombre: "",
      apellido: "",
      email: "",
      telefono: "",
    },
    cartel_insertar: "",
    cartel_update: "",
    cartel_delete: ""
  },
  methods: {
    sendDelete: function (id) {
      var deleteData = {
        data: {
          id: id
        }
      }
      axios.delete('/delete/', deleteData, this.axiosConfig)
        .then((res) => {
          console.log("Respuesta del delete: ", res);
          var i = 0;
          while (this.tasks[i]['id'] != res.data.usuario_eliminado['id']) {
            i++;
          }
          this.tasks.splice(i, 1);
          this.cartel_delete = "activo";

        }).catch((err) => {
          console.log("Error al borrar: ", err);
        });
    },
    sendPost: function (event) {
      axios.post('/create/', this.form, this.axiosConfig)
        .then((res) => {
          console.log("Respuesta del insert: ", res);
          app.tasks.push(res.data.consulta);
          this.form = {};
          this.cartel_insertar = "activo";
        })
        .catch((err) => {
          console.log("Error al querer insertar: ", err);
        })
    },
    sendUpdate: function (id) {
      var i = 0;
      while (app.tasks[i]['id'] != id) {
        i++;
      }
      axios.put('/update/', {
        nombre: app.tasks[i]['nombre'],
        apellido: app.tasks[i]['apellido'],
        email: app.tasks[i]['email'],
        telefono: app.tasks[i]['telefono'],
        id: id
      })
        .then(response => {
          console.log("Respuesta del update: ", response);
          this.cartel_update = "activo";
        })
        .catch(error => {
          console.log("Error al intentar updatear: ", error);
        });
    }
  },
  created() {
    axios.get('/read/')
      .then((response) => {
        app.tasks = response.data.tasks;
        console.log("respuesta del read: ", response.data.tasks);
      })
      .catch((error) => {
        console.log(error);
      });
  }
});

