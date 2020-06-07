import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {LoginComponent} from "./components/login/login.component";
import {RegisterComponent} from "./components/register/register.component";
import {FindUserComponent} from "./components/find-user/find-user.component";
import {StatusComponent} from "./components/status/status.component";
import {AddUserComponent} from "./components/add-user/add-user.component";
import {EnsureAuthenticatedService} from "./services/ensure-authenticated.service";

const routes: Routes = [
  {path: 'login', component: LoginComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'users', component: FindUserComponent, canActivate: [EnsureAuthenticatedService]},
  {path: 'users/create', component: AddUserComponent,  canActivate: [EnsureAuthenticatedService]},
  {path: 'users/:userId', component: StatusComponent, canActivate: [EnsureAuthenticatedService]},
  {path : '', component : LoginComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
