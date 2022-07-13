import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Item } from 'src/app/models/product';
import { ProductService } from 'src/app/services/product.service';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})
export class ProductComponent implements OnInit {

  item: any;
  id: any;
  // @Output() itemAdded = new EventEmitter;

  constructor(private productService: ProductService, private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.id= this.route.snapshot.paramMap.get('id');
    this.getProd();
  
  }
  getProd(): void {
     this.productService.GetDatabyId(this.id).subscribe((item) => {
      this.item=item;
     })
  }
  // addProductToCart(item) {
  //     this.itemAdded.emit(item);
  // }

}
