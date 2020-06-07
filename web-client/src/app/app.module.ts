import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { AuthService } from './services/auth.service';
import { HttpModule } from '@angular/http';
import { FormsModule } from "@angular/forms";
import { RegisterComponent } from './components/register/register.component';
import { StatusComponent } from './components/status/status.component';
import { UserManagementService } from "./services/user-management.service";
import { FindUserComponent } from './components/find-user/find-user.component';
import { AddUserComponent } from './components/add-user/add-user.component';
import { EnsureAuthenticatedService } from "./services/ensure-authenticated.service";

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    StatusComponent,
    FindUserComponent,
    AddUserComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpModule,
    FormsModule
  ],
  providers: [AuthService, UserManagementService, EnsureAuthenticatedService],
  bootstrap: [AppComponent]
})
export class AppModule { }
