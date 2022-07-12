import { Component, Input, OnInit } from '@angular/core';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { AuthService } from 'src/app/services/auth.service';
import { ProfileService } from 'src/app/services/profile.service';
import { Profile } from 'src/app/models/profile';
import { User } from 'src/app/models/auth';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-profile-update',
  templateUrl: './profile-update.component.html',
  styleUrls: ['./profile-update.component.css']
})
export class ProfileUpdateComponent implements OnInit {

  updateForm: UntypedFormGroup;
  @Input() profile!:any
  // profile: ;
  user: User
  userSub: Subscription;
  // profile: any;

  constructor(private authService: AuthService) { }

  ngOnInit(): void {
    this.userSub = this.authService.user.subscribe(
      (data:User) => {
        console.log(data);
        console.log(data.id)
        this.user = data
        console.log(this.user)
    
      })



    this.updateForm = new UntypedFormGroup({
      'bio': new UntypedFormControl(null,Validators.required),
      'phone_number': new UntypedFormControl(null,[
        Validators.required,
        Validators.pattern('^\d{10}$')
      
      ]),
    })
  }


  
  onSubmit(){
    console.log(this.updateForm)
    const form = this.updateForm.value

    this.userSub = this.authService.user.subscribe(
      (data:User) => {
        console.log(data);
        console.log(data.id)
        this.user = data
        console.log(this.user)
    
      })
  
  }

}
