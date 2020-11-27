module top;

    logic HCLK;
    logic HREASETn;

    logic [1:0] HTRANS;
    logic [2:0] HBURST;
    logic [3:0] HSIZE;
    logic       HWRITE;

    logic HREADY;

    logic [31:0] HADDR;
    logic [31:0] HWDATA;
    logic [31:0] HRDATA;

    logic HSELx=1;

    initial begin
        HCLK= 0;
        forever begin
            #5;
            HCLK= ~HCLK;
        end
    end

    initial begin
        HREASETn = 0;
        repeat(3) @(posedge HCLK);
        HREASETn = 1;
    end

    initial begin
        #100 $finish();
    end

    initial begin
        $dumpvars;
    end

    ahb_master master(.*);
    ahb_slave slave(.*);

endmodule

 typedef enum bit [1:0] {
    IDLE,
    NONSEQ,
    SEQ
} HTRANS_e;

typedef enum bit [3:0] {
BITS8,
BITS16,
BITS32
} HSIZE_e;

typedef enum bit [2:0] {
    SINGLE,
    INCR,
    WRAP4,
    INCR4,
    WRAP8,
    INCR8,
    WRAP16,
    INCR16
} HBURST_e;


module ahb_master(
    input wire HCLK,
    input wire HREASETn,

    output logic [1:0] HTRANS,
    output logic [2:0] HBURST,
    output logic [3:0] HSIZE,
    output logic       HWRITE,

    input wire HREADY,

    output logic [31:0] HADDR,
    output logic [31:0] HWDATA,
    input wire [31:0] HRDATA

);

// Write 
initial begin
    @(posedge HREASETn);
    @(posedge HCLK);
    // Set all control signals in address cycle
    #1 
    HBURST = NONSEQ;
    
    HBURST = SINGLE;
    HSIZE = BITS32; //word
    HWRITE = 1'b1;

    HADDR = 32'h38;
    HWDATA = 32'h138;
    
    @(posedge HCLK);
    // Start of data cycle

    @(posedge HCLK);
    // while(HREADY==0) begin
    //     @(posedge HCLK);
    // end
    $display($time,, "Transfer is Done");
end

endmodule

module ahb_slave(
    input wire HCLK,
    input wire HREASETn,

    input wire [1:0] HTRANS,
    input wire [2:0] HBURST,
    input wire [3:0] HSIZE,
    input wire       HWRITE,

    input wire HSELx,

    output logic HREADY,

    input wire [31:0] HADDR,
    input wire [31:0] HWDATA,
    output logic [31:0] HRDATA
);
endmodule
