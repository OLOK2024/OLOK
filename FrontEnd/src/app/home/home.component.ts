import { Component, OnInit } from '@angular/core';
import {RouterLink} from "@angular/router";
import {KeyService} from "../key.service";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    RouterLink,
    NgForOf,
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
  providers: [KeyService]
})
export class HomeComponent implements OnInit {
  passwordKeys: any;

  constructor(private keyService: KeyService) { }

  ngOnInit(): void {
    this.keyService.getPasswordKeys().subscribe({
      next: (keys) => {
        this.passwordKeys = keys;
      },
      error: (err) => {
        console.error('Error fetching password keys:', err);
      }
    });
  }
}
