import { Component, OnInit } from '@angular/core';
import {UntypedFormGroup, UntypedFormControl, Validators, FormBuilder, FormGroup, ControlContainer} from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { User } from '../models/auth';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent implements OnInit {
  
  user:User;
  isLoginMode=true;
  signupForm: UntypedFormGroup;
  loginForm: UntypedFormGroup;
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
    this.authService.signupUser({
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
        this.success='Signup was successful';
        this.error = null;
      },(errorRes)=>{
        console.log(errorRes);
        this.error=errorRes;
      }
    )
  }
  onLogin(){
    this.authService.loginUser(this.loginForm.value)
    .subscribe((response) => {

        this.authService.getProfile().subscribe((profile) => {
          this.router.navigate([`/home/`]);
        });
      }
      ,(errorRes)=>{
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


  // onLogin() {
  //   this.authService.loginUser(this.user).subscribe((user) => {
  //     console.log(user);
  //   });
  // }




}
