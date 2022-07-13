import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Item } from 'src/app/models/product';
import { ProductService } from 'src/app/services/product.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {


  @Input() list: any;
  id:number;
  // @Output() itemAdded = new EventEmitter;

  constructor(private productService: ProductService,private route: ActivatedRoute, private router: Router) { }

  ngOnInit(): void {
    this.productService.GetData().subscribe((item) => {
      console.log(item);
      this.list = item;
      console.log(this.list);
    })

  }
  // addProductToCart(item) {
  //   this.itemAdded.emit(item);
// }

}