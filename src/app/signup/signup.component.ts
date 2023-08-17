import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormGroup,FormBuilder, Validators, FormControl } from '@angular/forms';
import { Router } from '@angular/router';


@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  public signupForm!: FormGroup

  constructor(private formBuilder:FormBuilder, private http: HttpClient,private router: Router) { }

  ngOnInit(): void {
    this.signupForm = this.formBuilder.group({
      Name:['',Validators.required],
      Password:['',Validators.required,]
    })
  }

 

  onSubmit(){
    if(this.signupForm.valid){
    console.log(this.signupForm.value) 
    this.http.post<any>("http://127.0.0.1:5000/api/signup",this.signupForm.value)
    .subscribe(res=>{
      alert("signup successful !!!");
      this.signupForm.reset();
      this.router.navigate(["loginpage"]);
    }, err=>{console.log(err)
      alert("user already exists!!")
    })

    }
    else{
    
      this.validAllFormFields(this.signupForm)
      alert("Your form is invalid !!!")
    }

  }

  private validAllFormFields(formgroup:FormGroup){
    Object.keys(formgroup.controls).forEach(field=>{
      const control =formgroup.get(field);

      if(control instanceof FormControl){
        control.markAsDirty({onlySelf:true});
      }
      else if(control instanceof FormGroup){
        
        this.validAllFormFields(control)
      }
    })

  }
}



