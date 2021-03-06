import {login, logout} from "../actions/loginActions"
import auth from "../../authentification/auth";

export const fetchLogin = (passportNum, password) => {
  return dispatch => {
    fetch("http://localhost:5000/login", {
      method: "GET",
      credentials: "include",
      headers: {
        "Content-Type": "application/json;charset=utf-8",
        "passport_number": passportNum,
        "password": password
      }
    })
      .then((res => {
        return res.json()

      }))
      .then(data => {
        auth.setClientDataToLocalStorage(data.firstName, data.lastName)
        dispatch(login())
      })
    // todo return false if request is not successful
    return true
  }
}

export const fetchLogout = () => {
  return dispatch => {
    fetch("http://localhost:5000/logout", {
      method: "GET",
      credentials: "include",
      headers: {
        "Content-Type": "application/json;charset=utf-8",
      }
    })
      .then((res => {
        dispatch(logout())
        console.log(res)
      }))
    // todo return false if request is not successful

    return true
  }
}
