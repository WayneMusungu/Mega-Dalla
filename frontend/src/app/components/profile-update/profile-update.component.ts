import { Component, Input, OnInit } from '@angular/core';
import { NgForm, UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { AuthService } from 'src/app/services/auth.service';
import { ProfileService } from 'src/app/services/profile.service';
import { Profile } from 'src/app/models/profile';
import { User } from 'src/app/models/auth';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile-update',
  templateUrl: './profile-update.component.html',
  styleUrls: ['./profile-update.component.css']
})
export class ProfileUpdateComponent implements OnInit {

  updateForm: UntypedFormGroup;
  @Input() profile!:any

  constructor( private profileService: ProfileService, private router:Router) { }

  ngOnInit(): void {
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

    this.profileService.upDate(form).subscribe(data => {
      console.log(data)
      this.router.navigate(['/home']);
    });
  
  }

}
