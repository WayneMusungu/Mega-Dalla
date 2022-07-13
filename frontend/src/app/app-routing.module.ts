import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthComponent } from './auth/auth.component';
import { CheckoutComponent } from './components/checkout/checkout.component';
import { HomeComponent } from './components/home/home.component';
import { OrdersummaryComponent } from './components/ordersummary/ordersummary.component';
import { PaymentComponent } from './components/payment/payment.component';
import { ProductComponent } from './components/product/product.component';
import { ProfileUpdateComponent } from './components/profile-update/profile-update.component';
import { WelcomeComponent } from './components/welcome/welcome.component';
import { AuthGuard } from './guards/auth.guard';
import { ProfileComponent } from './profile/profile.component';
import { CartComponent } from './components/cart/cart.component';

const routes: Routes = [

  // { path: '', redirectTo: '/auth', pathMatch: 'full' },
  // { path: '**', redirectTo: '/auth' },


  {path: 'profile', component: ProfileComponent, canActivate: [AuthGuard]},
  {path: 'profile-update', component:ProfileUpdateComponent},
  {path: 'product/:id', component:ProductComponent},
  {path: 'checkout', component:CheckoutComponent},
  {path: 'payment', component:PaymentComponent},
  {path: 'ordersummary', component:OrdersummaryComponent},
  {path: 'home', component:HomeComponent},
  {path:'cart', component: CartComponent},
  // {path: 'welcome', component:WelcomeComponent},
  {path: '', component:WelcomeComponent},
  {path: 'auth', component:AuthComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }