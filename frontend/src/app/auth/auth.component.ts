import { Component, OnInit } from '@angular/core';
import {FormGroup, FormControl, Validators} from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { AuthResData } from '../models/auth.model';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent implements OnInit {
  
  isLoginMode=true;
  signupForm: FormGroup;
  loginForm: FormGroup;
  token: string;
  error:string=null;
  success:string=null;

  constructor(private authService: AuthService,private router: Router) { }

  ngOnInit(){
    this.signupForm = new FormGroup({
      'name': new FormControl(null,Validators.required),
      'username': new FormControl(null,Validators.required),
      'email': new FormControl(null,[Validators.required,Validators.email]),
      'passwords': new FormGroup({
        'password': new FormControl(null,[Validators.required,Validators.minLength(8)]),
        'confirmpassword': new FormControl(null, Validators.required)
      },this.passwordCheck)
    });
    this.loginForm = new FormGroup({
      'username': new FormControl(null,Validators.required),
      'password': new FormControl(null,[Validators.required,Validators.minLength(8)])
    })
  }

  onSwitch(){
    this.isLoginMode = !this.isLoginMode;
  }
  onSignup(){
    console.log(this.signupForm)
    this.authService.signup({
      'email': this.signupForm.get('email').value,
      'username': this.signupForm.get('username').value,
      'password': this.signupForm.get('passwords.password').value
    })
    .subscribe(
      (data) => {
        console.log(data)
        this.isLoginMode = true;
        this.success='Signup was successfull';
        this.error = null;
      },(errorRes)=>{
        console.log(errorRes);
        this.error=errorRes;
      }
    )
  }
  onLogin(){
    console.log(this.loginForm)
    this.authService.login(this.loginForm.value).subscribe((data) => {
        this.token = data.token
        console.log(data)
        this.router.navigate(['/profile'])
      },(errorRes)=>{
        this.error=errorRes;
      }
    )
    this.loginForm.reset()

  }
  passwordCheck(control: FormGroup): {[s:string]:boolean}{
    if(control.get('password').value != control.get('confirmpassword').value){
      return {'notsame': true}
    }
    return null;
  }

}
