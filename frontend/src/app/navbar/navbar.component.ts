import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { User } from '../models/auth';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  isAuthenticated:boolean = false;
  private userSub: Subscription;

  constructor(public authService: AuthService) { }

  ngOnInit() {
    this.userSub= this.authService.user.subscribe((user) =>{
      this.isAuthenticated=!user? false : true;
    })
  }
  ngOnDestroy() {
      this.userSub.unsubscribe();
  }
  onLogout(){
    this.authService.logout();
  }

}