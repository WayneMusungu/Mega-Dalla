import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { AuthService } from 'src/app/services/auth.service';
import { CartService } from 'src/app/services/cart.service';
// import { AuthService } from '../services/auth.service';
// import { User } from '../models/auth';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  totalItem : number = 0;
  isAuthenticated:boolean = false;
  private userSub: Subscription;

  constructor(public authService: AuthService, private cartService: CartService) { }

  ngOnInit() {
    this.userSub= this.authService.user.subscribe((user) =>{
      this.isAuthenticated=!user? false : true;
    })

    this.cartService.getProducts()
    .subscribe(res=>{
      this.totalItem = res.length;
    })
  }
  ngOnDestroy() {
      this.userSub.unsubscribe();
  }
  onLogout(){
    this.authService.logout();
  }

}
