import { Component, OnInit } from '@angular/core';
import { ProfileService } from '../profile.service';
import { Router } from "@angular/router";

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  profileData: any = {};

  constructor(private profileService: ProfileService, private router: Router) { }

  ngOnInit(): void {
    this.getProfileData();
  }

  getProfileData(): void {
    this.profileService.getProfile().subscribe({
      next: (profileData) => {
        this.profileData = profileData;
        console.log('Profile data:', this.profileData);
        this.fillFormFields();
      },
      error: (err) => {
        console.error('Error fetching bunch of keys:', err);
      }
    });
  }

  fillFormFields(): void {
    // Fill the form fields with the profile data
    (document.getElementById('profileLastName') as HTMLInputElement).value = this.profileData.last_name;
    (document.getElementById('profileFirstName') as HTMLInputElement).value = this.profileData.first_name;
    (document.getElementById('profileCountry') as HTMLSelectElement).value = this.profileData.country_code;
    (document.getElementById('profileStartTime') as HTMLInputElement).value = this.profileData.start_of_day;
    (document.getElementById('profileEndTime') as HTMLInputElement).value = this.profileData.end_of_day;
    (document.getElementById('profileWorkDays') as HTMLInputElement).value = this.profileData.workdays;
  }

  updateProfile(): void {
    const firstName = (document.getElementById('profileFirstName') as HTMLInputElement).value;
    const lastName = (document.getElementById('profileLastName') as HTMLInputElement).value;
    const country = (document.getElementById('profileCountry') as HTMLSelectElement).value;
    const startTime = (document.getElementById('profileStartTime') as HTMLInputElement).value;
    const endTime = (document.getElementById('profileEndTime') as HTMLInputElement).value;
    const workDays = (document.getElementById('profileWorkDays') as HTMLInputElement).value.toString();
    this.profileService.updateProfileInfo(firstName, lastName, country, startTime, endTime, workDays).subscribe({
      next: () => {
        console.log('Profile updated successfully');
      },
      error: (err) => {
        console.error('Error updating profile:', err);
      }
    });
  }

  updatePassword(): void {
    const oldPassword = (document.getElementById('oldPassword') as HTMLInputElement).value;
    const newPassword = (document.getElementById('newPassword') as HTMLInputElement).value;
    const confirmNewPassword = (document.getElementById('confirmNewPassword') as HTMLInputElement).value;
    this.profileService.updatePassword(oldPassword, newPassword, confirmNewPassword).subscribe({
      next: () => {
        console.log('Password updated successfully');
      },
      error: (err) => {
        console.error('Error updating password:', err);
      }
    });
  }

  deleteProfile(): void {
    this.profileService.deleteProfile().subscribe({
      next: () => {
        console.log('Profile deleted successfully');
        localStorage.removeItem('token');
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.error('Error deleting profile:', err);
      }
    });
  }

  backToDashboard(): void {
    this.router.navigate(['/home']);
  }

}
