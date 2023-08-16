import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormGroup, FormBuilder, Validators, FormControl } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-loginpage',
  templateUrl: './loginpage.component.html',
  styleUrls: ['./loginpage.component.css']
})
export class LoginpageComponent implements OnInit {
  public loginform!: FormGroup;
  private isLoggedIn = false;

  constructor(
    private formbuilder: FormBuilder,
    private http: HttpClient,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loginform = this.formbuilder.group({
      Name: ['', Validators.required],
      Password: ['', Validators.required]
    });
    this.checkLoginStatus().then(isLoggedIn => {
      this.isLoggedIn = isLoggedIn;
    });
  }


  login(): void {
    if (this.loginform.valid) {
      this.http.post("http://127.0.0.1:5000/api/login", this.loginform.value)
        .subscribe(res => {
          console.log(res);
          const response: any = res;
          if (response.success) {
            alert("Login success!");
            this.loginform.reset();
            this.isLoggedIn = true;
            this.router.navigate(['salespredict']);
          } else {
            alert("Login failed!");
          }
        }, err => {
          alert("Login failed!");
        });
    } else {
      this.validAllFormFields(this.loginform);
      alert("Your form is invalid!");
    }
  }

  private validAllFormFields(formgroup: FormGroup): void {
    Object.keys(formgroup.controls).forEach(field => {
      const control = formgroup.get(field);

      if (control instanceof FormControl) {
        control.markAsDirty({ onlySelf: true });
      } else if (control instanceof FormGroup) {
        this.validAllFormFields(control);
      }
    });
  }

  private checkLoginStatus(): Promise<boolean> {
    return new Promise<boolean>((resolve, reject) => {
      this.http.get("http://127.0.0.1:5000/api/check_login_status")
        .subscribe(
          (res: any) => {
            console.log(res);
            resolve(res.isLoggedIn);
          },
          (err: any) => {
            console.error(err);
            reject(err);
          }
        );
    });
  }
}
  