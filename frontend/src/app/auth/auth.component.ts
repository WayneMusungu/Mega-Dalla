import { Component, OnInit } from '@angular/core';
import {UntypedFormGroup, UntypedFormControl, Validators} from '@angular/forms';
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
  signupForm: UntypedFormGroup;
  loginForm: UntypedFormGroup;
  token: string;
  error:string=null;
  success:string=null;

  constructor(private authService: AuthService,private router: Router) { }

  ngOnInit(){
    this.signupForm = new UntypedFormGroup({
      'username': new UntypedFormControl(null,Validators.required),
      'email': new UntypedFormControl(null,[Validators.required,Validators.email]),
      'is_vendor': new UntypedFormControl(null),
      'is_customer': new UntypedFormControl(null),
      'passwords': new UntypedFormGroup({
        'password': new UntypedFormControl(null,[Validators.required,Validators.minLength(6)]),
        'confirmpassword': new UntypedFormControl(null, Validators.required)
      },this.passwordCheck)
    });
    this.loginForm = new UntypedFormGroup({
      'username': new UntypedFormControl(null,Validators.required),
      'password': new UntypedFormControl(null,[Validators.required,Validators.minLength(6)])
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
      'is_vendor': this.signupForm.get('is_vendor').value,
      'is_customer': this.signupForm.get('is_customer').value,
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
  passwordCheck(control: UntypedFormGroup): {[s:string]:boolean}{
    if(control.get('password').value != control.get('confirmpassword').value){
      return {'notsame': true}
    }
    return null;
  }

}
