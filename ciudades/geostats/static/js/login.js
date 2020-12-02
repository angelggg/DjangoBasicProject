function CheckForm(){

	var name = document.getElementById("uname").value;
	var pwd  = document.getElementById("pwd").value;
	flag = false;

	if (name  == "" ){
		document.getElementById("uname-error").innerHTML = "Please insert a name";
		flag = true
	}	else	{
				document.getElementById("uname-error").innerHTML = "";
	}
		
	if (pwd.length < 8 ){
		document.getElementById("pwd-error").innerHTML = "Passwords are 8 or more characters long";
		flag = true
	}	else	{
		document.getElementById("pwd-error").innerHTML = "";

	}
	if (!flag)
		document.getElementById("login-form").submit();
	}