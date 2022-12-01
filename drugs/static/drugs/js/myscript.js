
function toggleTabCd(){
	var entry = document.querySelector("form div select");
	var labels = document.querySelectorAll("form div label");
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

var handle = document.querySelector("form div select");
//handle.onclick = toggleTabCd();

handle.addEventListener("click", toggleTabCd);

var drugName = document.querySelector("div #div_id_drug_name input");
var brandName = document.querySelector("div #div_id_brand_name input");
var weight = document.querySelector("div div_id_weight input");
var priceLabel = document.querySelector("label#sale-price");

if (drugName && brandName && weight){
	priceLabel.innerText = "$"
}
