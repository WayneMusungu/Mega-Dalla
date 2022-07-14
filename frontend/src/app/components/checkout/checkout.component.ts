import { Component, OnInit } from '@angular/core';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { User } from 'src/app/models/auth';
import { AddressService } from 'src/app/services/address.service';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.css']
})
export class CheckoutComponent implements OnInit {

  checkoutForm: UntypedFormGroup;

  // user:User;

  constructor(private addressService: AddressService, private authService: AuthService) { }

  ngOnInit(): void {
    this.checkoutForm = new UntypedFormGroup({
      'street_address': new UntypedFormControl(null,Validators.required),
      'apartment_address': new UntypedFormControl(null,Validators.required),
      'country': new UntypedFormControl(null,Validators.required),
      'zip': new UntypedFormControl(null,Validators.required),
      'address_type': new UntypedFormControl(null,Validators.required),
      'default': new UntypedFormControl(null)
      // 'user': new UntypedFormControl(null,Validators.required),
      // 'user': this.user.value(),
    })

  }
  onSubmit(){
    console.log(this.checkoutForm)
    this.addressService.checkoutdata({
      'street_address': this.checkoutForm.get('street_address').value,
      'apartment_address': this.checkoutForm.get('apartment_address').value,
      'country': this.checkoutForm.get('country').value,
      'zip': this.checkoutForm.get('zip').value,
      'address_type': this.checkoutForm.get('address_type').value,
      'default': this.checkoutForm.get('default').value,
      // 'user':this.user.

    }).subscribe((data) => {
      console.log(data);})
  }

}
