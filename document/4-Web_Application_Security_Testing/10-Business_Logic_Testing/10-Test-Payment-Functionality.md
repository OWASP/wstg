# Test Payment Functionality

|ID          |
|------------|
|WSTG-BUSL-10|

## Summary

TODO

## Test Objectives

- TODO

## How to Test

### Quantity Tampering

Most e-commerce websites allow users to add items to a basket before they start the checkout process. This basket should keep track of which items that have been added, and the item of each item. The quality should normally be a positive integer, but if the website does not properly validate this then it may be possible to a decimal quantity of an item (e.g, 0.1) or a negative quantity (e.g, -1). Depending on the backend processing, adding negative quantities of an item may result in a negative value, reducing the overall cost of the basket.

There are usually multiple ways to modify the contents, of the basket that should be tested, such as:

- Adding a negative quantity of an item.
- Repeatedly removing items until the quantity is negative.
- Updating the quantity to a negative value.

Some sites may also provide a drop-down menu of valid quantities (such as items that must be bought in packs of 10), and it may be possible to tamper these requests to add other numbers of items.

If the full basket details are passed to the payment gateway (rather than simply passing a total value), it may also be possible to tamper the values at that stage.

### Price Tampering

#### On the Application

When adding an item to the basket, the application should only include the item and a quantity, such as the example request below:

```http
POST /api/basket/add HTTP/1.1
Host: example.org

item_id=1&quantity=5
```

However, in some cases the application may also include the price, meaning that it may be possible to tamper it:

```http
POST /api/basket/add HTTP/1.1
Host: example.org

item_id=1&quantity=5&price=2.00
```

Different types of items may have different validation rules, so eac type needs to be separately testing. For example, some applications allow users to add an optional donation to charity as part of their purchase, and this donation can usually be an arbitrary amount. If this amount is not validated, it may be possible to add a negative donation amount, which would then reduce the total value of the basket.

#### On the Payment Gateway

If the checkout process is performed on an external payment gateway, then it may be possible to tamper with the prices between the application and the gateway.

For example, the transfer to the gateway may be performed using a cross-domain POST to the gateway, as shown in the HTML example below (note that the card details are not included - the user will be prompted for them on the payment gateway):

```html
<form action="https://example.org/process_payment" method="POST">
    <input type="hidden" id="merchant_id" value="123" />
    <input type="hidden" id="basket_id" value="456" />
    <input type="hidden" id="item_id" value="1" />
    <input type="hidden" id="item_quantity" value="5" />
    <input type="hidden" id="item_total" value="20.00" />
    <input type="hidden" id="shipping_total" value="2.00" />
    <input type="hidden" id="basket_total" value="22.00" />
    <input type="hidden" id="currency" value="GBP" />
    <input type="submit" id="submit" value="submit" />
</form>
```

By modifying the HTML form or intercepting the POST request, it may be possible to modify the prices of items, and to effectively purchase them for less. Note that many payment gateway will reject a transaction with a value of zero, to a total of 0.01 is more likely to succeed. However, some payment gateways may accept negative values, which could be used to steal money from the application. Where there are multiple values (such as item prices, a shipping cost and the total basket cost), all of these should be tested.

If the payment gateway uses an iframe instead, it may be possible to perform a similar type of attack by modifying the IFRAME URL:

```html
<iframe src="https://example.org/payment_iframe?merchant_id=123&basket_total=22.00" />
```

Note that the payment gateway is usually run by a third-party, and as such may not be included in the scope of testing. This means that while price tampering may be acceptable, other types of attacks (such as SQL injection) should not be performed without explicit written approval).

#### Encrypted Transaction Details

In order to prevent the transaction being tampered with, some payment gateways will encrypt the details of the request that is made to them. For example, [Paypal](https://developer.paypal.com/api/nvp-soap/paypal-payments-standard/integration-guide/encryptedwebpayments/#link-usingewptoprotectmanuallycreatedpaymentbuttons) do this using public key cryptography.

The first thing to try is making an unencrypted request, as some payment gateways allow insecure transactions unless a specific configuration option has been set.

If this doesn't work, then you need to find the public key that is used to encrypt the transaction details, which could be exposed in a backup of the application, or if you can find a directory traversal vulnerability.

Alternatively, it's possible that the application re-uses the same public/private key pair for the payment gateway and it's digital certificate. You can obtain the public key from the server with the following command:

```bash
echo -e '\0' | openssl s_client -connect example.org:443 2>/dev/null | openssl x509 -pubkey -noout
```

Once you have this key, you can then try and create an encrypted request (based on the payment gateway's documentation), and submit it to the gateway to see if it's accepted.

#### Secure Hashes

Other payment gateway use a secure hash (or HMAC) of the transaction details to prevent tampering. The exact details of how this is done will vary between providers (for example, [Adyen](https://docs.adyen.com/online-payments/classic-integrations/hosted-payment-pages/hmac-signature-calculation) use HMAC-SHA256), but it will normally include the details of the transaction and a secret value. For example, a hash may be calculated as:

```php
$secure_hash = md5($merchant_id . $transaction_id . $items . $total_value . $secret)
```

This value is then added to the POST request that is sent to the payment gateway, and verified to ensure that the transaction hasn't been tampered with.

The first thing to try is removing the secure hash, as some payment gateways allow insecure transactions unless a specific configuration option has been set.

The POST request should contain all of the values required to calculate this hash, other than the secret key. As such, if you know how the hash is calculated (which should be included in the payment gateway's documentation), then you can attempt to brute-force the secret. Alternatively, if the website is running an off-the-shelf application, there may be a default secret in the configuration files or source code. Alternatively, if you can find a backup of the website, or otherwise gain access to the configuration files, you may be able to find the secret there.

If you can obtain this secret, you can then tamper the transaction details, and then generate your own secure hash which will be accepted by the payment gateway.

#### Currency Tampering

If it's not possible to tamper with the actual prices, it may be possible to change the currency that is used, especially where applications support multiple currencies. For example, the application may validate that the price is 10, but if you can change the currency so that you pay 10 USD rather than 10 GBP, this would allow you to purchase items more cheaply.

#### Time Delayed Requests

If the value of items on the site changes over time (for example on a currency exchange), then it may be possible to buy or sell at an old price by intercepting requests using a local proxy and delaying them. In order for this to be exploitable, the price would need to either be included in the request, or linked to something in the request (such as session or transaction ID). The example below shows how this could potentially be exploited on a application that allows users to buy and sell gold:

- View the current price of gold on the website.
- Initiate a buy request for 1oz of gold.
- Intercept the request.
- Wait one minutes to check the price of gold again:
    - If it increases, allow the transaction to complete, and buy the gold for less than it's current value.
    - If it decreases, drop the request request.

### Discount Codes

If the application supports discount codes, then there are various checks that should be carried out:

- Are the codes easily guessable (TEST, TEST10, SORRY, SORRY10, company details, etc)?
- Is there any brute-force protection?
- Can multiple discount codes be applied at once?
- Can discount codes be applied multiple times?
- Can you [inject wildcard characters](07-Input_Validation_Testing/05-Testing_for_SQL_Injection.md#sql-wildcard-injection) such as `%` or `*`?
- Are discount codes exposed in the HTML source, in or hidden `<input>` fields anywhere on the application?

In addition to these, the usual vulnerabilities such as SQL injection should be tested for.

### Breaking Payment Flows

- Modifying details during process (items, address, etc)
- Modifying details after checkout is completed
- Many payment flows include redirection:
    - Checkout on application
    - Redirected to third-party to make payment
    - Redirected back to `success.php` or `fail.php` depending on status
- Can you get redirected, then force-browse to success page?
- Can you make multiple requests to success page?
- Does success page include an ID? IDOR

### Exploiting Transaction Processing Fees

- Merchants have to pay fees for every transaction processed
    - Usually fixed fee + percentage
- Very small transaction ($0.01) usually cost merchant money to receive
- Check minimum transaction values

### Testing Logistics

- If testing in live, may result in real transactions
- Get client to cancel and refund (processing fees?)
- If testing in dev/staging, get test payment cards
- Keep careful track of any transactions made

### PCI DSS

- Standard that covers card payments
- Any application taking payments should be compliant
- Requirements depend on how payments are made (see [Visa Guidance](https://www.visa.co.uk/dam/VCOM/regional/ve/unitedkingdom/PDF/risk/processing-e-commerce-payments-guide-73-17337.pdf)):
    - SAQ A: redirect or IFRAME
    - SAQ A-EP: cross-domain POST
    - SAQ D: cardholder data touches server
- SAQ A is best choice, should flag clients not doing that
- Flag if cardholder data is stored and can be viewed/retrieved

### Test Payment Cards

- Most payment gateways have test cards - can these be used?
    - [Adyen](https://docs.adyen.com/development-resources/test-cards/test-card-numbers)
    - [Globalpay](https://developer.globalpay.com/resources/test-card-numbers)
    - [Stripe](https://stripe.com/docs/testing)
    - [Worldpay](http://support.worldpay.com/support/kb/bg/testandgolive/tgl5103.html)

## Related Test Cases

- TODO

## Remediation

- Use a redirect or IFRAME wherever possible.
- Handle all payment information on server-side:
    - Only things client-side should be item ID and quantity
- Review payment gateway documentation and use all available security features
- Ensure that application payment flow is robust

## Tools

- Intercepting proxy

## References

- TODO
