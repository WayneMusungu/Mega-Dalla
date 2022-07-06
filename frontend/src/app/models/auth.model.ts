export interface signupModel{
    email: string,
    username: string,
    password: string,
    is_vendor: boolean,
    is_customer:boolean,
}

export interface AuthResData{
    id: number,
    email: string,
    username: string,
    is_vendor: boolean,
    is_customer:boolean,

    token?: string
}

export interface loginModel{
    username: string,
    password: string
}

export class User{
    constructor(
       
        public id: number,
        public email: string,
        public username: string,
        public is_vendor: boolean,
        public is_customer:boolean,
    ){}
    
}