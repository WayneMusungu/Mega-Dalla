import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { User } from '../models/auth';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit, OnDestroy{

  user: User
  userSub: Subscription;

  constructor(private authService: AuthService) { }

  ngOnInit() { 
    this.userSub = this.authService.user.subscribe(
    (data:User) => {
      console.log(data);
      console.log(data.id)
      this.user = data
      console.log(this.user)
    })
  }
  ngOnDestroy(){
    this.userSub.unsubscribe()
  }

}
