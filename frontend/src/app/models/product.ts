export interface Product {
    id?: number;
    title: string;
    price: number;
    discountPrice?: number;
    category: string;
    label: string;
    description: string;
    image: string;
}