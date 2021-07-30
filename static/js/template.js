//點選登入
function clicksignin(){
    let msg = document.getElementById("errmsg_login");
    msg.style.display = "none";
    document.getElementById("id_email").value="";
    document.getElementById("id_pwd").value="";
    let modal = document.getElementById("myModal");
    let close = document.getElementById("close");
    let signup_content = document.getElementById("signup_content");
    signup_content.style.display = "none"
    let signin_content = document.getElementById("signin_content");
    signin_content.style.display = "block"
    modal.style.display = "block";
    close.onclick = function()
    {
        modal.style.display = "none";
    }

    window.onclick = function(event) 
    {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}


//點選 [還沒有帳戶？點此註冊]
function signup(){
    let msg = document.getElementById("errmsg");
    msg.style.display = "none";
    let modal = document.getElementById("myModal");
    let signin_content = document.getElementById("signin_content");
    signin_content.style.display = "none"
    let signup_content = document.getElementById("signup_content");
    signup_content.style.display = "block"
    let signupclose = document.getElementById("signupclose");
    
    document.getElementById("sign_name").value="";
    document.getElementById("sign_email").value="";
    document.getElementById("sign_pwd").value="";
    signupclose.onclick = function()
    {
        modal.style.display = "none";
    }
    window.onclick = function(event) 
    {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

//已有帳號要回登入頁面
function haveAccount(){
    document.getElementById("id_email").value="";
    document.getElementById("id_pwd").value="";
    let modal = document.getElementById("myModal");
    let signin_content = document.getElementById("signin_content");
    signin_content.style.display = "block"
    let signup_content = document.getElementById("signup_content");
    signup_content.style.display = "none"
    let close = document.getElementById("close");
    close.onclick = function()
    {
        modal.style.display = "none";
    }
    window.onclick = function(event) 
    {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

//BTN sign_up
function btn_signup(){
    let req = new XMLHttpRequest();
    let name = document.getElementById("sign_name").value;
    let email = document.getElementById("sign_email").value;
    let pwd = document.getElementById("sign_pwd").value;
    if (name== "" || email == "" || pwd=="")
    {
        let msg = document.getElementById("errmsg");
        msg.style.display = "block";
        msg.innerHTML="空格為必填";
    }
    else
    {
        if(email.includes("@"))
        {
            let msg = document.getElementById("errmsg");
            msg.style.display = "none";
            req.open("POST","/api/user?email="+email+"&name="+name+"&password="+pwd)
            console.log("/api/user?email="+email+"&name="+name+"&password="+pwd)
            req.setRequestHeader('Content-type', 'application/json');
            req.onload = function () 
            {
                let data = JSON.parse(this.response);
                if(Object.keys(data)[0] != "error")
                {
                    let msg = document.getElementById("errmsg");
                    msg.style.display = "block";
                    msg.innerHTML="註冊成功";
                }
                else
                {
                    let msg = document.getElementById("errmsg");
                    msg.style.display = "block";
                    msg.innerHTML=data["message"];
                }
            }
            req.send();
        }
        else
        {
            let msg = document.getElementById("errmsg");
            msg.style.display = "block";
            msg.innerHTML="信箱格式錯誤";
                
        }
       
    }
}


//BTN sign_in
function btn_signin(){
    let email = document.getElementById("id_email").value;
    let pwd = document.getElementById("id_pwd").value;
    if(email == "" || pwd =="")
    {
        let msg = document.getElementById("errmsg_login");
        msg.style.display = "block";
        msg.innerHTML="空格為必填"
    }
    else
    {
        let req = new XMLHttpRequest();
        req.open("PATCH","/api/user?email="+email+"&password="+pwd)
        req.onload = function () 
        {
            let data = JSON.parse(this.response);
            if(Object.keys(data)[0] == "error")
            {
                let msg = document.getElementById("errmsg_login");
                msg.style.display = "block";
                msg.innerHTML=data["message"];
            }
            else
            {
                location.reload();
            }
        }
        req.send();
     }
}

function myFunction(){
    let email = document.getElementById("id_email").value;
    let pwd = document.getElementById("id_pwd").value;
    if(email == "" || pwd =="")
    {
        let msg = document.getElementById("errmsg_login");
        msg.style.display = "block";
        msg.innerHTML="空格為必填"
    }
    else
    {
        let req = new XMLHttpRequest();
        req.open("PATCH","/api/user?email="+email+"&password="+pwd)
        req.onload = function () 
        {
            let data = JSON.parse(this.response);
            if(Object.keys(data)[0] == "error")
            {
                let msg = document.getElementById("errmsg_login");
                msg.style.display = "block";
                msg.innerHTML=data["message"];
            }
            else
            {
                location.reload();
            }
        }
        req.send();
     }
}

//click log_out
function clicksignout()
{
    let req = new XMLHttpRequest();
    req.open("DELETE","/api/user")
    req.onload = function () 
        {
            let data = JSON.parse(this.response);
            if(Object.keys(data)[0] == "ok")
            {
                location.reload();
            }
        }
        req.send();
}

//到預定行程
function gobooking(){
    let book="book";
    checkuser(book);
}

//確認登入狀態
function checkuser(page){
    //check user verified
   let req = new XMLHttpRequest();
   req.open("GET","/api/user")
   req.send();
   req.onload = function()
   {
       let data = JSON.parse(this.response);
       console.log(data["data"])
       if(data["data"] != null)
       {
           let signin = document.getElementById("signin");
           signin.style.display="none";
           let signout = document.getElementById("signout");
           signout.style.display="block";
           if(page == "book")
           {
               self.location="/booking";
           }
       }
       else
       {
           let signin = document.getElementById("signin");
           signin.style.display="block";
           let signout = document.getElementById("signout");
           signout.style.display="none";
           if(page == "book")
           {
               clicksignin();
           }
       }
   }
}

//回到首頁(台北一日遊)
function returnIndex()
{
   self.location="/";
}