#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "led_strip.h"
#include "sdkconfig.h"
#include "esp_sleep.h"

static const char *TAG = "example";

#define BLINK_GPIO CONFIG_BLINK_GPIO
#define BTN_GPIO   4

static uint8_t s_led_state = 0;
static volatile bool sleep_enabled = false;

#ifdef CONFIG_BLINK_LED_STRIP
static led_strip_handle_t led_strip;

static void blink_led(void)
{
    if (s_led_state) {
        led_strip_set_pixel(led_strip, 0, 0, 0, 255); // Azul
        led_strip_refresh(led_strip);
    } else {
        led_strip_clear(led_strip);
        led_strip_refresh(led_strip);
    }
}

static void configure_led(void)
{
    ESP_LOGI(TAG, "Configurando LED Strip");
    led_strip_config_t strip_config = {
        .strip_gpio_num = BLINK_GPIO,
        .max_leds = 1,
    };

#if CONFIG_BLINK_LED_STRIP_BACKEND_RMT
    led_strip_rmt_config_t rmt_config = {
        .resolution_hz = 10 * 1000 * 1000,
        .flags.with_dma = false,
    };
    ESP_ERROR_CHECK(led_strip_new_rmt_device(&strip_config, &rmt_config, &led_strip));
#else
#error "unsupported LED strip backend"
#endif

    led_strip_clear(led_strip);
    led_strip_refresh(led_strip);
}
#else
#error "This example requires LED STRIP"
#endif

/* ========= ISR DEL BOTÓN ========= */
static void IRAM_ATTR gpio_isr_handler(void *arg)
{
    sleep_enabled = !sleep_enabled; // Toggle seguro en ISR
}

/* ========= CONFIG BOTÓN ========= */
static void configure_button(void)
{
    gpio_config_t btn_cfg = {
        .pin_bit_mask = (1ULL << BTN_GPIO),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = 1,
        .pull_down_en = 0,
        .intr_type = GPIO_INTR_NEGEDGE
    };
    gpio_config(&btn_cfg);

    gpio_install_isr_service(0);
    gpio_isr_handler_add(BTN_GPIO, gpio_isr_handler, NULL);
}

void app_main(void)
{
    configure_led();
    configure_button();

    ESP_LOGI(TAG, "Sistema listo: RGB + Light Sleep toggle");

    while (1) {
        if (!sleep_enabled) {
            // Modo normal: parpadeo LED
            ESP_LOGI(TAG, "LED %s", s_led_state ? "ON" : "OFF");
            blink_led();
            s_led_state = !s_led_state;
            vTaskDelay(pdMS_TO_TICKS(CONFIG_BLINK_PERIOD));
        } else {
            // Modo sleep
            ESP_LOGI(TAG, "Entrando en LIGHT SLEEP");

            // Apagar LED antes de dormir
            led_strip_clear(led_strip);
            led_strip_refresh(led_strip);

            // Configurar wake-up por GPIO
            esp_sleep_enable_gpio_wakeup();
            gpio_wakeup_enable(BTN_GPIO, GPIO_INTR_LOW_LEVEL);

            // Entrar en light sleep
            esp_light_sleep_start();

            ESP_LOGI(TAG, "Desperté del LIGHT SLEEP");
        }
    }
}
