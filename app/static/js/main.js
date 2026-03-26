// permet de visualiser le mot de passe 
function togglePassword() {
    const input = document.getElementById('password');
    const icon  = document.getElementById('eyeIcon');
    if (input.type === 'password') {
      input.type = 'text';
      icon.className = 'bi bi-eye-slash-fill';
    } else {
      input.type = 'password';
      icon.className = 'bi bi-eye-fill';
    }
  }

  function showSection(id, el) {
    document
      .querySelectorAll(".dash-section")
      .forEach((s) => s.classList.remove("active"));
    document
      .querySelectorAll(".sb-link")
      .forEach((b) => b.classList.remove("active"));
    document.getElementById("section-" + id).classList.add("active");
    el.classList.add("active");
  }
  function openModal(id) {
    document.getElementById(id).classList.add("open");
    document.body.style.overflow = "hidden";
  }
  function closeModal(id) {
    document.getElementById(id).classList.remove("open");
    document.body.style.overflow = "";
  }
  document.querySelectorAll(".modal-overlay").forEach((o) => {
    o.addEventListener("click", (e) => {
      if (e.target === o) closeModal(o.id);
    });
  });
  function confirmDelete(name, route, id) {
    document.getElementById("delete-name").textContent = name;
    document.getElementById("btn-delete").href = "/" + route + "/" + id;
    openModal("modal-delete");
  }
  function filterTable(input, id) {
    const v = input.value.toLowerCase();
    document.querySelectorAll("#" + id + " tbody tr").forEach((r) => {
      r.style.display = r.textContent.toLowerCase().includes(v) ? "" : "none";
    });
  }

  function closeAlert(id) {
    document.getElementById(id).style.display = "none";
  }

  function openEditModalApp(id, N_App, etage, Superficie, type, status) {
    document.getElementById("edit-id").value = id;
    document.getElementById("edit-N_App").value = N_App;
    document.getElementById("edit-etage").value = etage;
    document.getElementById("edit-Superficie").value = Superficie;
    document.getElementById("edit-type").value = type;
    document.getElementById("edit-status").value = status;
    openModal("modal-edit-apt");
  }
  
  function openEditModalLoc(id,Nom,Prenom, Tel,Email,NumeroRue,Rue,NumeroApp,ville,province,code) {
   
    console.log("element:", document.getElementById("edit-id"));
    document.getElementById("edit-id_loc").value = id;
    document.getElementById("edit-Nom").value = Nom;
    document.getElementById("edit-Prenom").value = Prenom;
    document.getElementById("edit-Tel").value = Tel;
    document.getElementById("edit-Email").value = Email;
    document.getElementById("edit-Rue").value =Rue;
    document.getElementById("edit-NumeroRue").value = NumeroRue;
    document.getElementById("edit-NumeroApp").value = NumeroApp;
    document.getElementById("edit-ville").value = ville;
    document.getElementById("edit-province").value = province;
    document.getElementById("edit-code").value = code;
    


    openModal("modal-edit-loc");
  }
  //modifier un administrateur

  function openEditModalAdmin(id,Prenom,Nom,Email,Role) {
   
    
    document.getElementById("edit-id-admin").value = id;
    document.getElementById("ed-Prenom").value = Prenom;
    document.getElementById("ed-Nom").value = Nom;
    document.getElementById("ed-Email").value = Email;
    // document.getElementById("ed-Password").value =Password;
    document.getElementById("ed-Role").value = Role;

    openModal("modal-edit-admin");
  }

function showAlert(message) {
  document.getElementById("alert-msg").innerText = message;
  document.getElementById("alert-strip").style.display = "flex";
}


//   function validateApp() {
//   const N_App = document.querySelector('[name="N_App"]').value.trim();
//   const etage = document.querySelector('[name="etage"]').value.trim();
//   const Superficie = document.querySelector('[name="Superficie"]').value.trim();

//   if (!N_App) {
//     showAlert("Le numéro d'appartement est obligatoire");
//     return false;
//   }

//   if (!etage) {
//     showAlert("L'étage est obligatoire");
//     return false;
//   }

//   if (!Superficie || Superficie <= 0) {
//     showAlert("La superficie doit être supérieure à 0");
//     return false;
//   }

//   return true; 
// }

document.addEventListener("DOMContentLoaded", function () {
  
  const today = new Date().toISOString().split("T")[0];

  const date_debut = document.getElementById("date_debut");
  const date_fin = document.getElementById("date_fin");

  if (date_debut) date_debut.min = today;
  if (date_fin) date_fin.min = today;

});

function setMinDateFin() {
  const debut = document.getElementById("date_debut").value;
  if (debut) {
    document.getElementById("date_fin").min = debut;
  }
}


function validateRealTime(fieldId, errorId, message, condition) {
  const field = document.getElementById(fieldId);
  const error = document.getElementById(errorId);

  field.addEventListener("input", function () {
    if (condition(field.value)) {
      error.style.display = "none";
      field.style.borderColor = "#0d9488"; // vert
    } else {
      error.style.display = "block";
      field.style.borderColor = "#dc2626"; // rouge
    }
  });
}

// Utilisation
document.addEventListener("DOMContentLoaded", function () {
  
  // Valider email
  validateRealTime(
    "email",
    "error-email",
    "Email invalide",
    (val) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)
  );

  // Valider téléphone
  validateRealTime(
    "Tel",
    "error-tel",
    "Téléphone invalide",
    (val) => val.length >= 10
  );

  // Valider champ non vide
  validateRealTime(
    "Nom",
    "error-nom",
    "Nom obligatoire",
    (val) => val.trim() !== ""
  );

});




document.addEventListener("DOMContentLoaded", function () {

  // Validation temps réel appartement
  const apFields = [
    { id: "N_App",      errorId: "error-N_App",      check: (v) => v.trim() !== "" },
    { id: "etage",      errorId: "error-etage",      check: (v) => v.trim() !== "" },
    { id: "Superficie", errorId: "error-Superficie", check: (v) => v > 0 }
  ];

  apFields.forEach(({ id, errorId, check }) => {
    const field = document.getElementById(id);
    const error = document.getElementById(errorId);
    if (!field) return;

    field.addEventListener("input", function () {
      if (check(field.value)) {
        error.style.display = "none";
        field.style.borderColor = "#0d9488"; // vert
      } else {
        error.style.display = "block";
        field.style.borderColor = "#dc2626"; // rouge
      }
    });
  });

});

// Validation avant soumission
function validateApp() {
  let valid = true;

  const apFields = [
    { id: "N_App",      errorId: "error-N_App",      check: (v) => v.trim() !== "" },
    { id: "etage",      errorId: "error-etage",      check: (v) => v.trim() !== "" },
    { id: "Superficie", errorId: "error-Superficie", check: (v) => v > 0 }
  ];

  apFields.forEach(({ id, errorId, check }) => {
    const field = document.getElementById(id);
    const error = document.getElementById(errorId);
    if (!check(field.value)) {
      error.style.display = "block";
      field.style.borderColor = "#dc2626";
      valid = false;
    }
  });

  return valid; // false = bloque l'envoi
}
