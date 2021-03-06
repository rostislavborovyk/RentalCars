import React, {Fragment, useEffect, useState} from "react";
import {NavLink} from 'react-router-dom';
import auth from "../../authentification/auth";
import {store} from "../../index";
import {connect} from "react-redux";

const NavBar = (state) => {
  const [render, setRender] = useState(false);

  useEffect(() => {
    const unsubscribe = store.subscribe(() => {
        setRender(!render)
      }
    )
    return unsubscribe
  }, [])


  const selectName = (state) => {
    return `${state.login.firstName} ${state.login.lastName}`
  }

  const showLoginAndRegister = () => {
    return (
      <ul className="navbar-nav mr-sm-2">
        <li className="nav-item">
          <NavLink
            className="nav-link"
            to="/login"
          >
            Login
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink
            className="nav-link"
            to="/register"
          >
            Register
          </NavLink>
        </li>
      </ul>
    )
  }

  const showLogout = () => {
    return (
      <ul className="navbar-nav mr-sm-2 name-navbar">
        <li className="nav-item nav-name-container">
          <small className="nav-name-elem">{selectName(store.getState())}</small>
        </li>
        <li className="nav-item">
          <NavLink
            className="nav-link"
            to="#"
            onClick={async () => await auth.logout()}
          >
            Logout
          </NavLink>
        </li>

      </ul>
    )
  }

  return (
    <Fragment>
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <a className="navbar-brand" href="/">RentalCars</a>
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarText"
                aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
          <ul className="navbar-nav mr-auto">
            <li className="nav-item">
              <NavLink
                className="nav-link"
                to="/orders"
              >
                Orders
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink
                className="nav-link"
                to="/clients"
              >
                Clients
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink
                className="nav-link"
                to="/cars"
              >
                Cars
              </NavLink>
            </li>
          </ul>
        </div>
        <div>
          {!auth.isAuthentificated() ? (
            showLoginAndRegister()
          ) : (
            showLogout()
          )}
        </div>
      </nav>
    </Fragment>
  )
}

export default connect(
  state => ({
    state: state
  })
)(NavBar)
