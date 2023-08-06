<%inherit file="${context['logintpl']}" />
<div class="row">
    <div class="${bc['xs']}12">
      <form action="${request.route_url('ppss:user:changepassword')}" method="POST" class="ppssauthform">
          <h2>Change password for user ${request.loggeduser.username}</h2>
          <input type="password" name="oldpassword" placeholder="current password">
          <br/>
          <input type="password" name="newpassword" placeholder="new password">
          <br/>
          <input type="password" name="confirmnewpassword" placeholder="confirm new password">
          <br/>
          <div class="text-center">
            <input type="submit" name="submit" value="entra"/>
          </div>

          <p>${msg}</p>
      </form>
    </div>
</div>
