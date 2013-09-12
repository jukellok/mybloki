function validateLogin() {
	if (document.getElementById("usernamefield").value == "" || document.getElementById("passwordfield").value == "") {
		return false;
	} else {
		return true;
	}
}

function validatePost() {
	if (document.getElementById("titlefield").value == "" || document.getElementById("contentfield").value == "") {
		return false;
	} else {
		return true;
	}
}

function validateTag() {
	if (document.getElementById("tagfield").value == "" ) {
		return false;
	} else {
		return true;
	}
}
