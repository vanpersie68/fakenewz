<template>
  <div class="form-content">
    <meta name="viewport" content="width-device-width, initial-scale=1.0" />
    <Tabs>
      <hr />
      <!-- Display Profile Details -->
      <Tab name="Profile details" selected="true">
        <div class="user-details">
          <br />
          <div id="saved-username">{{ $t('g5.profile-username') }}</div>
          <br />
          <div id="saved-email">{{ $t('g5.profile-email') }}</div>
          <br />
          <div id="saved-firstname">{{ $t('g5.profile-first') }}</div>
          <br />
          <div id="saved-lastname">{{ $t('g5.profile-last') }}</div>
        </div>
        <button @click="logoutAction" class="logout">
          {{ $t('g5.logout') }}
        </button>
      </Tab>
      <!-- Update Profile Settings -->
      <Tab name="Update profile">
        <div class="update-profile-window">
          <form class="update-settings">
            <br />
            <div class="row">
              <div class="column">
                <p class="msg">{{ $t('g5.update-first') }}:</p>
                <input type="text" id="fname" :placeholder="$t('g5.enterFirstName')" v-model="first_name" />

                <p class="msg">{{ $t('g5.update-last') }}:</p>
                <input type="text" id="lname" :placeholder="$t('g5.enterLastName')" v-model="last_name" />
              </div>
              <div class="column">
                <p class="msg">{{ $t('g5.old-password') }}:</p>
                <div>
                  <input type="password" id="cpassword" :placeholder="$t('g5.enterCurrentPassword')"
                    v-model="old_password" ref="password1" />
                  <font-awesome-icon class="eye" v-show="show" @click="showPasswords" icon="eye" />
                  <font-awesome-icon class="eye" v-show="!show" @click="showPasswords" icon="eye-slash" />
                </div>

                <p class="msg">{{ $t('g5.new-password') }}:</p>
                <div>
                  <input type="password" id="npassword" :placeholder="$t('g5.enterNewPassword')" v-model="new_password1"
                    ref="password2" />
                  <font-awesome-icon class="eye" v-show="show" @click="showPasswords" icon="eye" />
                  <font-awesome-icon class="eye" v-show="!show" @click="showPasswords" icon="eye-slash" />
                </div>

                <p class="msg">{{ $t('g5.confirm-password') }}:</p>
                <div>
                  <input type="password" id="confirmnpassword" :placeholder="$t('g5.confirmPassword')"
                    v-model="new_password2" ref="password3" />
                  <font-awesome-icon class="eye" v-show="show" @click="showPasswords" icon="eye" />
                  <font-awesome-icon class="eye" v-show="!show" @click="showPasswords" icon="eye-slash" />
                </div>
              </div>
            </div>
          </form>
          <div id="container">
            <button @click="editDetails" class="save">
              {{ $t('g5.save') }}
            </button>
            <button @click="confirm" class="delete">
              {{ $t('g5.delete-account') }}
            </button>
            <button @click="update" class="update">
              {{ $t('g5.update-pwd') }}
            </button>
          </div>
        </div>
      </Tab>
    </Tabs>
  </div>
</template>

<script>
import pubsub from 'pubsub-js'
import Tab from '@/components/Tab'
import Tabs from '@/components/Tabs'

export default {
  name: 'User',
  data() {
    return {
      old_password: '',
      new_password1: '',
      new_password2: '',
      show: false,
    }
  },
  methods: {
    logoutAction() {
      this.$axios
        .post('account/logout/', {
          headers: {
            Authorization: 'Token ' + localStorage.getItem('token'),
          },
        })
        .then((res) => {
          alert('Logout successfully', res)
          //update user status
          pubsub.publish('logoutAction', false)
          //remove token when logout
          localStorage.removeItem('token')
          //redirect to the login page
          this.$router.replace({
            name: 'login',
          })
        })
        .catch((reason) => {
          alert('Logout failed' + reason)
        })
    },
    getUserInfo() {
      this.$axios
        .get('account/user/', {
          headers: {
            Authorization: 'Token ' + localStorage.getItem('token'),
          },
        })
        .then((response) => {
          document.getElementById('saved-username').innerHTML =
            this.$t('g5.profile-username') + ': ' + response.data.username
          document.getElementById('saved-email').innerHTML =
            this.$t('g5.profile-email') + ': ' + response.data.email
          document.getElementById('saved-firstname').innerHTML =
            this.$t('g5.profile-first') + ': ' + response.data.first_name
          document.getElementById('saved-lastname').innerHTML =
            this.$t('g5.profile-last') + ': ' + response.data.last_name
        })
        .catch((reason) => {
          this.$swal('Could not fetch user info: ' + reason)
          this.$router.replace({
            name: 'home',
          })
        })
    },
    // /*edit first and last name
    editDetails() {
      this.$axios
        .post(
          'account/update/',
          {
            first_name: this.first_name,
            last_name: this.last_name,
          },
          {
            headers: {
              Authorization: 'Token ' + localStorage.getItem('token'),
            },
          }
        )
        .then((response) => {
          document.getElementById('saved-firstname').innerHTML =
            'First name: ' + this.first_name
          document.getElementById('saved-lastname').innerHTML =
            'Last name: ' + this.last_name
          console.log(response)
          this.first_name = ''
          this.last_name = ''
          window.location.reload()
        })
        .catch((reason) => {
          alert('Cannot update first and last name ' + reason)
        })
    },
    confirm() {
      this.$swal({
        title: 'ATTENTION!',
        text: 'Deleting your account will remove all accociated data. You can visit My Surveys to export survey data first.',
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: this.$t('g5.My Surveys'),
        denyButtonText: this.$t('g5.delete-account'),
        cancelButtonText: this.$t('g5.cancel'),
      }).then((result) => {
        if (result.isConfirmed) {
          this.$router.replace({
            name: 'mySurvey',
          })
        } else if (result.isDenied) {
          this.$swal({
            title: this.$t('g5.delete-account'),
            text: 'Are you sure you want to delete your account? This action cannot be undone.',
            icon: 'warning',
            showCancelButton: true,
            showDenyButton: true,
            denyButtonText: this.$t('g5.delete-account'),
            cancelButtonText: this.$t('g5.cancel'),
            showConfirmButton: false,
          }).then((result2) => {
            if (result2.isDenied) {
              this.deleteAccount()
            }
          })
        }
      })
    },
    deleteAccount() {
      this.$axios
        .delete('account/delete/', {
          headers: {
            Authorization: 'Token ' + localStorage.getItem('token'),
          },
        })
        .then((res) => {
          alert('Account deleted', res)
          //update user status
          pubsub.publish('logoutAction', false)
          //remove token when deleting account
          localStorage.removeItem('token')
          //redirect to the home page
          this.$router.replace({
            name: 'index',
          })
        })
        .catch((reason) => {
          alert('Account deletion failed' + reason)
        })
    },
    update() {
      this.$axios
        .post(
          'account/password/change/',
          {
            old_password: this.old_password,
            new_password1: this.new_password1,
            new_password2: this.new_password2,
          },
          {
            headers: {
              Authorization: 'Token ' + localStorage.getItem('token'),
            },
          }
        )
        .then((response) => {
          alert('Password updated successfully.')
          console.log(response)
          this.old_password = ''
          this.new_password1 = ''
          this.new_password2 = ''
          window.location.reload()
        })
        .catch((err) => {
          let error = err.response.data.Message
          let errorMessage = ''
          for (let i = 0; i < error.length; i++) {
            if (error[i] === 1) {
              errorMessage = errorMessage + this.$t('resetpwd.msg1')
            }
            if (error[i] === 2) {
              errorMessage = errorMessage + this.$t('resetpwd.msg2')
            }
            if (error[i] === 3) {
              errorMessage = errorMessage + this.$t('resetpwd.msg3')
            }
            if (error[i] === 4) {
              errorMessage = errorMessage + this.$t('resetpwd.msg4')
            }
            if (error[i] === 5) {
              errorMessage = errorMessage + this.$t('resetpwd.msg5')
            }
            if (error[i] === 6) {
              errorMessage = errorMessage + this.$t('resetpwd.msg6')
            }
            if (error[i] === 7) {
              errorMessage = errorMessage + this.$t('resetpwd.msg7')
            }
          }
          alert(errorMessage)
        })
    },
    showPasswords() {
      if (this.show == false) {
        this.$refs.password1.type = 'text'
        this.$refs.password2.type = 'text'
        this.$refs.password3.type = 'text'
        this.show = !this.show
      } else {
        this.$refs.password1.type = 'password'
        this.$refs.password2.type = 'password'
        this.$refs.password3.type = 'password'
        this.show = !this.show
      }
    },
  },
  beforeMount() {
    this.getUserInfo()
  },
  components: {
    Tab,
    Tabs,
  },
  // beforeRouterEnter(to,from,next) {
  //   console.log('Enter user profile',to,from)
  //   if(to.meta.isAuth) {

  //   }
  // }
}
</script>

<style scoped>
.form-content {
  background-color: white;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  color: black;
  font-size: 16px;
}

.user-details {
  font-size: 16px;
  color: black;
  margin-left: 2%;
}

/* #update-settings {
  background-color: white;
  border-radius: 16px;
  padding: 20px 0 18px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: absolute;
  left: 500px;
  bottom: 70px;
} */
.update-profile-window {
  margin-left: 2%;
}
.msg {
  font-family: 'Arial';
  font-size: 16px;
}

#uname,
#fname,
#lname,
#email,
#npassword,
#confirmnpassword,
#cpassword {
  display: inline;
  height: 30px;
  padding: 5px 5px;
  color: #000000;
  background-color: #ffffff;
  border: 1px solid #eeeeee;
  border-radius: 5px;
  font-size: 16px;
  margin-bottom: 1px;
}

.save,
.logout,
.update {
  font-size: 15px;
  margin-top: 20px;
  margin-bottom: 30px;
  display: inline-block;
  padding: 0.75rem;
  border: 2px solid black;
  border-radius: 2px;
  cursor: pointer;
  border: 0;
  margin-left: 2%;
}

.delete {
  background-color: rgb(255, 80, 80);
  font-size: 15px;
  margin-top: 20px;
  margin-bottom: 20px;
  display: inline-block;
  padding: 0.75rem;
  border: 2px solid black;
  border-radius: 2px;
  cursor: pointer;
  border: 0;
  margin-left: 17px;
}

.delete:hover,
.save:hover,
.logout:hover {
  opacity: 0.5;
}

#container {
  text-align: left;
  display: block;
  position: relative;
  top: 20%;
}

.column {
  float: left;
  margin-left: 2%;
}

.row:after {
  content: '';
  display: table;
  clear: both;
}

.eye {
  margin-left: 11px;
  cursor: pointer;
}
</style>
