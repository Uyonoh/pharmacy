
function toggleTabCd(){
	entry = document.querySelector("form div select");
	labels = document.querySelectorAll("form div label");
	console.log("clicked");

	if (entry.value != "Tab"){
		//entry.classList.add("hidden");
		//labels[4].classList.add("hidden");
		labels[4].innerText = "Bottles";
	} else {
		//labels[4].classList.remove("hidden");
		labels[4].innerText = "Tab cd*";
	}
}

handle = document.querySelector("form div select");
//handle.onclick = toggleTabCd();

handle.addEventListener("click", toggleTabCd);

drugName = Document.querySelector("div #div_id_drug_name input");

drugName.value = "retty";

priceLabel = Document.querySelector("label #sale-price");
