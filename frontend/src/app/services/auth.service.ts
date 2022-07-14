import { Injectable } from "@angular/core";
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { catchError,map,tap} from 'rxjs/operators';
import { BehaviorSubject, Observable, throwError } from "rxjs";
import { Router } from "@angular/router";
import { loginModel, signupModel, User, Userr } from "../models/auth";
import { environment } from "src/environments/environment";
import { Profile } from "../models/profile";


@Injectable({providedIn: 'root'})
export class AuthService{

    private _isLoggedin = new BehaviorSubject<boolean>(false);

    isLoggedin=this._isLoggedin.asObservable();

    user = new BehaviorSubject<Userr>(null);
    private initialUser: any = null;
  private profileSource: BehaviorSubject<Profile> = new BehaviorSubject(
    this.initialUser
  );

  public profile = this.profileSource.asObservable();

    private url = `${environment.apiUrl}`;

    constructor(private http: HttpClient, private route: Router) {
      this.profileSource.next(this.getLocalStorage('profile'));
      const token = localStorage.getItem('accessToken');
      this._isLoggedin.next(!!token);
    }

    signupUser(user: signupModel){
      return this.http.post<User>(`${this.url}/signup/`,user)
      .pipe(catchError(this.handleError),tap((res)=>{
        console.log(res)
      }))
    }

    loginUser(account: loginModel){
      return this.http.post<any>(`${this.url}/login/`,account)
        .pipe(catchError(this.handleError),tap((res)=>{
          console.log(res);
          this.setToken(res);
          this.handleAuth(res);
          this.getProfile().subscribe();
        return this.profile.subscribe((user) => user);
        }))
    }
    getProfile(): Observable<Profile> {
      return this.http.get<Profile>(`${this.url}/profile`).pipe(
        map((profile: any) => {
          console.log(profile)
          this.setLocalStorage('profile', profile);
          this.profileSource.next(profile);
          return profile;
        })
      );
    }
    autologin(){
      const userData:User = JSON.parse(localStorage.getItem('user'))
      console.log(userData)
      if(!userData){
        return;
      }
      const loadedUser = new Userr(userData.id,userData.email,userData.username,userData.is_vendor, userData.is_customer)
      this.user.next(loadedUser)
      console.log(loadedUser)
      return;
    }

    private handleError(error: HttpErrorResponse){
      console.log(error)
      let errormessage = 'An unknown errror occured'
      if(!error.error){
          return throwError(errormessage)
      }
      if(error.error.non_field_errors){
          errormessage = error.error.non_field_errors[0]
      }
      if(error.error.email){
          errormessage = error.error.email[0]
      }
      if(error.error.username){
          errormessage = error.error.username[0]
      }
      return throwError(errormessage);
    }

    private handleAuth(res: User){
      const user = new Userr(res.id,res.email,res.username,res.is_vendor, res.is_customer);
      this.user.next(user);
      console.log(user)
      localStorage.setItem('user',JSON.stringify(user))
      this._isLoggedin.next(true);
    }


    logout(){
      this.user.next(null)
      this.removeLocalStorage();
      this.route.navigate(['/'])
    }

  setToken(token: any): void {
    this.setLocalStorage('accessToken', token.access);
    this.setLocalStorage('refreshToken', token.refresh);

    // decode the token to read the user_id and expiration timestamp
    const accessTokenParts = token.access.split('.');
    const refreshTokenParts = token.refresh.split('.');
    const accessToken = JSON.parse(window.atob(accessTokenParts[1]));
    const refreshToken = JSON.parse(window.atob(refreshTokenParts[1]));
    this.setLocalStorage('accessExpiry', new Date(accessToken.exp * 1000));
    this.setLocalStorage('refreshExpiry', new Date(refreshToken.exp * 1000));
  }

  setLocalStorage(key: string, value: any) {
    if (key === 'profile') value = JSON.stringify(value);
    localStorage.setItem(key, value);
    return this.getLocalStorage(key);
  }

  removeLocalStorage() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('profile');
    localStorage.removeItem('accessExpiry');
    localStorage.removeItem('refreshExpiry');
    localStorage.removeItem('user');
    return this.getLocalStorage('accessToken');
  }
  getLocalStorage(key: string): any {
    const item = localStorage.getItem(key);
    if (key === 'profile' && item != null) return JSON.parse(item);
    return item;
  }
}