

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

function showAlert(message) {
  document.getElementById("alert-msg").innerText = message;
  document.getElementById("alert-strip").style.display = "flex";
}


  function validateApp() {
  const N_App = document.querySelector('[name="N_App"]').value.trim();
  const etage = document.querySelector('[name="etage"]').value.trim();
  const Superficie = document.querySelector('[name="Superficie"]').value.trim();

  if (!N_App) {
    showAlert("Le numéro d'appartement est obligatoire");
    return false;
  }

  if (!etage) {
    showAlert("L'étage est obligatoire");
    return false;
  }

  if (!Superficie || Superficie <= 0) {
    showAlert("La superficie doit être supérieure à 0");
    return false;
  }

  return true; 
}

