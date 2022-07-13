import { Component, OnInit, Input } from '@angular/core';
import { Item } from 'src/app/models/product';
import { ProductService } from 'src/app/services/product.service';
import { CartService } from 'src/app/services/cart.service';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})
export class ProductComponent implements OnInit {
  @Input() product:Item;

  item!: Item;
  constructor(private productService: ProductService, private cartService: CartService) { }

  ngOnInit(): void {

    this.productService.GetData().subscribe((item) => {
      console.log(item);
      this.item = item;
    })
  }

  addtocart(item: any){
    this.cartService.addtoCart(item);
  }

}
