'use strict';

var stripe = Stripe('pk_test_fEJG3FbEEKCGhriUfqjWJZG5');

function submit_token(token, card, email, post_id, example) {
    $.ajax({
        url: base_url + 'token/',
        type: 'POST',
        contentType: "application/json",
        datatype: "json",
        data:  JSON.stringify({
            "token": token,
            "card": card,
            "email": email,
            "post_id": post_id,
        }),
        error: function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseText);
        },
        success: function(res) {
          example.classList.add('submitted');
        },
        complete: function() {
          example.classList.remove('submitting');
        }
    });
}

function registerElements(elements, exampleName) {
    var formClass = '.' + exampleName;
    var example = document.querySelector(formClass);

    var form = example.querySelector('form');
    var resetButton = example.querySelector('a.reset');
    var error = form.querySelector('.error');
    var errorMessage = error.querySelector('.message');

    function enableInputs() {
      Array.prototype.forEach.call(
        form.querySelectorAll(
          "input[type='text'], input[type='email'], input[type='tel']"
        ),
        function(input) {
          input.removeAttribute('disabled');
        }
      );
    }

    function disableInputs() {
      Array.prototype.forEach.call(
        form.querySelectorAll(
          "input[type='text'], input[type='email'], input[type='tel']"
        ),
        function(input) {
          input.setAttribute('disabled', 'true');
        }
      );
    }

    // Listen for errors from each Element, and show error messages in the UI.
    var savedErrors = {};
    elements.forEach(function(element, idx) {
      element.on('change', function(event) {
        if (event.error) {
          error.classList.add('visible');
          savedErrors[idx] = event.error.message;
          errorMessage.innerText = event.error.message;
        } else {
          savedErrors[idx] = null;

          // Loop over the saved errors and find the first one, if any.
          var nextError = Object.keys(savedErrors)
            .sort()
            .reduce(function(maybeFoundError, key) {
              return maybeFoundError || savedErrors[key];
            }, null);

          if (nextError) {
            // Now that they've fixed the current error, show another one.
            errorMessage.innerText = nextError;
          } else {
            // The user fixed the last error; no more errors.
            error.classList.remove('visible');
          }
        }
      });
    });

    // Listen on the form's 'submit' handler...
    form.addEventListener('submit', function(e) {
      e.preventDefault();

      // Show a loading screen...
      example.classList.add('submitting');

      // Disable all inputs.
      disableInputs();

      // Gather additional customer data we may have collected in our form.
      var name = form.querySelector('#' + exampleName + '-name');
      var email = form.querySelector('#' + exampleName + '-email');
      var address = form.querySelector('#' + exampleName + '-address');
      var post_id = $("#post-id").val();
      var additionalData = {
        name: name ? name.value : undefined,
        address_line1: address ? address.value : undefined,
      };

      // Use Stripe.js to create a token. We only need to pass in one Element
      // from the Element group in order to create a token. We can also pass
      // in the additional customer data we collected in our form.
      stripe.createToken(elements[0], additionalData).then(function(result) {
        if (result.token) {
          // If we received a token, show the token ID.
          submit_token(
              result.token.id, result.token.card, email, post_id, example);
        } else {
          // Otherwise, un-disable inputs.
          example.classList.remove('submitting');
          enableInputs();
        }
      });
    });
}

function add_elements() {
    'use strict';

    var elements = stripe.elements({
      fonts: [
        {
          cssSrc: 'https://fonts.googleapis.com/css?family=Roboto',
        },
      ],
      // Stripe's examples are localized to specific languages, but if
      // you wish to have Elements automatically detect your user's locale,
      // use `locale: 'auto'` instead.
      locale: window.__exampleLocale
    });

    var card = elements.create('card', {
      iconStyle: 'solid',
      style: {
        base: {
          iconColor: '#c4f0ff',
          color: '#fff',
          fontWeight: 500,
          fontFamily: 'Roboto, Open Sans, Segoe UI, sans-serif',
          fontSize: '15px',
          fontSmoothing: 'antialiased',

          ':-webkit-autofill': {
            color: '#fce883',
          },
          '::placeholder': {
            color: '#87BBFD',
          },
        },
        invalid: {
          iconColor: '#FFC7EE',
          color: '#FFC7EE',
        },
      },
    });
    card.mount('#example1-card');

    registerElements([card], 'example1');
}
