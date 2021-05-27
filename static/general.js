
//  Local Storage and body classes
if (typeof(Storage) !== "undefined") {
	
	var el = document.getElementById('body');
	var themeText = document.getElementById('currentTheme');
	var theme = localStorage.theme;
    
	if( theme == "dark") {
		el.classList.add("dark");
		themeText.innerHTML = "Dark";
	}else{
		el.classList.remove("dark");
		themeText.innerHTML = "Classic";
		localStorage.theme = "classic";
	}
	
	
	// Click to change theme class, localstorage theme
	function changeTheme(themeName){

		if( themeName == "dark") {
			localStorage.theme = "dark";
			themeText.innerHTML = "Dark";
			el.classList.add(localStorage.getItem("theme"));
		}else{
			localStorage.theme = "classic";
			el.classList.remove("dark");
			themeText.innerHTML = "Classic";
		}

	}	
	
}

