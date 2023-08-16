import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginpageComponent } from './loginpage/loginpage.component';
import { PagenotfoundComponent } from './pagenotfound/pagenotfound.component';
import { SalespredictComponent } from './salespredict/salespredict.component';
import { SalesreportComponent } from './salesreport/salesreport.component';
import { SignupComponent } from './signup/signup.component';
import { HomeComponent } from './home/home.component';

const routes: Routes = [
  {path:'',component:HomeComponent},
  {path:'home', component:HomeComponent},
  {path:'loginpage',component:LoginpageComponent},
  {path:'signup',component: SignupComponent}, 
  {path:'salespredict',component: SalespredictComponent},
  {path:'salesreport', component:SalesreportComponent},
  {path:'**',component: PagenotfoundComponent}   
  

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
