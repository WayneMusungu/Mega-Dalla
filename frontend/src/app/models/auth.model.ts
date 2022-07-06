export interface signupModel{
    email: string,
    username: string,
    password: string,
    
    // roles:[]
}

export interface AuthResData{
    id: number,
    email: string,
    username: string,
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
        public token?: string,
    ){}
    
}