import axios from "axios";
import { useEffect, useRef, useState } from "react";
import config from '../../config.json';
import Cookies from 'js-cookie';
import decodeToken from "../../utils/decodeToken.js";
const Profile = () => {
        
    const [picture,setPicture] = useState("")
    const token = decodeToken(Cookies.get('token'));
    const [fname,setFname] = useState(token.first_name?token.first_name:"")
    const [lname, setLname]= useState(token.last_name?token.last_name:"")
    const [username, setUsername] = useState(token.username)
    const [bio, setBio] = useState(token.bio?token.bio:"");
    const [phone ,setPhone] = useState(token.phone_number?token.phone_number:"");
    useEffect(()=>{
       
        console.log(token)
        
        
    },[])
    const convertToBase64 = (file) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => {
            setPicture(reader.result);
        };
        reader.onerror = (error) => {
            console.error('Error converting file to base64:', error);
        };
    };

    
    const handleFileChange = (event)=>{
        const file = event.target.files[0];
        if (file) {
            convertToBase64(file);
        }
        

    }
    const saveHandler = ()=>{
        
        const url = `${config.url}/profile`
        const data = {
            'profile_picture': picture,
            'first_name':fname==token.first_name?"":fname,
            'last_name':lname==token.last_name?"":lname,
            'username':username==token.username?"":username,
            'bio':bio==token.bio?"": bio,
            'phone_number':phone==token.phone_number?"":phone,
            'token':Cookies.get('token')
        }        
        axios.post(url,data).then(res=>{
            console.log("Good")
            console.log(decodeToken(res.data.token))

            Cookies.set('token',res.data.token);
        }).catch(err=>console.log("what"))
    }

    return (
        <div className="profile">
            <input type="file" className="picture" onChange={handleFileChange} />
            <input type="text" className="fname"  value={fname} onChange={(e)=>{setFname(e.target.value)}} placeholder="First name"/>
            <input type="text" className="lname"  value={lname} onChange={(e)=>{setLname(e.target.value)}} placeholder="Last name"/>
            <input type="text" className="username"  value={username} onChange={(e)=>{setUsername(e.target.value)}} placeholder="Username"/>
            <input type="text" className="bio"  value={bio} onChange={(e)=>{setBio(e.target.value)}} placeholder="Bio"/>
            <input type="text" className="phone"  value={phone} onChange={(e)=>{setPhone(e.target.value)}} placeholder="Phone number"/>

            <button onClick={saveHandler}>Save</button>
        </div>

    )
}

export default Profile;